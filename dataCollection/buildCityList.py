"""
Script to build dict of static data on cities in a given country
"""

# Imports
from screenScrape import Scraper
import json
import requests 
import csv
import sys
from bs4 import BeautifulSoup

# Constants
googleAPIKey = 'AIzaSyBw0StR76cWn1lE3laP23Tr9zig47bC-K8'
validCountries = set(["Italy", "France", "Croatia", "Germany"])


###### HOSTELS ######


# Function to find provence and city URLs / names
def fetchOtherLocations(urls, provencePage):
    links = []
    for url in urls:
        s = Scraper(url)
        container = s.search('div', klass='otherlocations')
        otherLocations = (s.search('a', html=container[0]) if provencePage else s.search('a', portion='href', html=container[0]))
        for link in otherLocations:
            if provencePage:
                links.append((link.text, link.get('href')))
            else:
                links.append(link)
    return links

# Function to build initial map of cities for certain country 
# based off hostelworld.com url of country's base page
def buildCityMap(url, country):
    provences = fetchOtherLocations([url], False)
    print('Starting provences')
    cities = fetchOtherLocations(provences, True)
    print('Finished provences')
    cities.sort(key=lambda city: city[0])
    cityMap = {}
    for city in cities:
        cityMap[city[0]] = [country, city[1]]
    return cityMap


###### POPULATION ######


# Function to add the population data for each city to the city map
def addPopulationData(country, cityMap):
    url = 'https://population.mongabay.com/population/' + country.lower() + '/'
    s = Scraper(url)
    rows = s.search('tr')
    for row in rows:
        [link, pop] = s.search('td', html=row)
        city = link.find('a').text
        if city in cityMap:
            cityMap[city].append(int(pop.text.replace(',', '')))

# Function to prune all communes from city data
def prune(cityMap, val):
    communes = set()
    for key in cityMap:
        if len(cityMap[key]) < val:
            communes.add(key)
    for key in communes:
        del cityMap[key]


###### COORDINATES ######


# Function to add coordinate infor for each city to the map
def addCoordData(cityMap):
    for key in cityMap:
        city = key.replace(' ', '+')
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city + ',+'
        url += cityMap[key][0] + '&key=' + googleAPIKey
        response = requests.get(url)
        data = response.json()
        cityMap[key].append(data['results'][0]['geometry']['location']['lat'])
        cityMap[key].append(data['results'][0]['geometry']['location']['lng'])


###### WEATHER ######

#Helper function to get all countries 
def getCountries(base_url):
    europe_url = base_url + '/europe/'
    response = requests.get(europe_url)
    soup = BeautifulSoup(response.content, 'html5lib')
    article = soup.find('div', id='article')
    countries_li = article.find_all('li')
    countries = []
    for country_li in countries_li:
        link = country_li.find('a')
        countries.append((link.text, link['href']))

    return countries

#Helper function to get all regions
def getRegions(base_url, country_base_url):
    country_url = base_url + country_base_url
    response = requests.get(country_url, 'html5lib')
    soup = BeautifulSoup(response.content, 'html5lib')
    article = soup.find('div', id='article')
    regions_li = article.find_all('li')
    regions = []
    for region_li in regions_li:
        link = region_li.find('a')
        regions.append((link.text, link['href']))

    return regions

# Helper function to get all cities
def getCities(base_url, region_base_url, page=''):
    region_url = base_url + region_base_url + page
    response = requests.get(region_url, 'html5lib')
    soup = BeautifulSoup(response.content, 'html5lib')
    data = soup.find('div', id='article')
    link_elems = data.find_all('a')
    cities = []
    for link_elem in link_elems:
        link = link_elem['href']
        name = link_elem.find('span', class_='name').text
        cities.append((name, link))

    pages = soup.find('div', class_='pagination')
    page_links = pages.find_all('a')
    last_link = page_links[-1]
    if last_link.text == 'Next':
        next_page_url = last_link['href']
        next_page_url = next_page_url[2:]
        cities += getCities(base_url, region_base_url, next_page_url)

    return cities

#Scrape city page for weather info
def scrapeCityWeather(base_url, city_base_url):
    city_url = base_url + city_base_url
    response = requests.get(city_url, 'html5lib')
    soup = BeautifulSoup(response.content, 'html5lib')
    table = soup.find('table', id='weather_table')
    rows = table.find_all('tr')

    weather = {}
    for row in rows[4:]:
        entries = row.find_all('td')
        if len(entries) > 0:
            description = entries[0].text
            data = [elem.text.replace('\n', '') for elem in entries[1:]]
            
            description = description.split(' ')[0].replace('.', '')
            weather[description] = data
    
    return weather

#Use helper functions above to add weather to each city 
def addWeather(supported_cities, cur_country):

    base_url = 'https://en.climate-data.org'
    countries = getCountries(base_url)

    regions = []
    for country in countries:
        name = country[0]
        url = country[1]
        if name == cur_country:
            regions += getRegions(base_url, url)

    cities = []
    for region in regions:
        name = region[0]
        url = region[1]
        cities += getCities(base_url, url)

    weather_cities = {entry[0]:entry[1] for entry in cities}

    for city in supported_cities:
        if city in weather_cities:
            city_weather = scrapeCityWeather(base_url, weather_cities[city])
            supported_cities[city].append(city_weather)
        #TODO: Map cities without weather data to nearest city that does have data
        else: 
            supported_cities[city].append("No information available")

###### MAIN FUNCTIONS ######


def writeToFile(data, filename):
    string = json.dumps(data)
    f = open(filename, 'w+')
    f.write(string)
    f.close()

def main(country):
    url = 'https://www.hostelworld.com/hostels/' + country.lower()
    cities = buildCityMap(url, country)
    print("Done with hostelworld scraping")
    addPopulationData(country, cities)
    print("Done with population scraping")
    prune(cities, 3)
    addCoordData(cities)
    print("Done with coordinate scraping")
    addWeather(cities, country)
    print("Done with weather scraping")
    fileName = '../database/countries/' + country.lower() + 'Data.txt'
    writeToFile(cities, fileName)

# Add checks for valid input country
if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1][0].islower():
        sys.stderr.write("Please give the country of interest\nProper format is python3 buildCityList.py Country\n")
    elif sys.argv[1] not in validCountries:
        sys.stderr.write("That country is currently not supported\n")
    else:
        main(sys.argv[1])

