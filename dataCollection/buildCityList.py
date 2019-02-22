# Imports
from screenScrape import Scraper
import json
import requests 
import csv
import sys

# Constants
googleAPIKey = 'AIzaSyBw0StR76cWn1lE3laP23Tr9zig47bC-K8'


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
def buildCityMap(url):
    provences = fetchOtherLocations([url], False)
    print('Starting provences')
    cities = fetchOtherLocations(provences, True)
    print('Finished provences')
    cities.sort(key=lambda city: city[0])
    cityMap = {}
    for city in cities:
        cityMap[city[0]] = ['Italy', city[1]]
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
        if city in italianCities:
            italianCities[city].append(int(pop.text.replace(',', '')))

# Function to prune all communes from city data
def prune(cityMap, val):
    communes = set()
    for key in italianCities:
        if len(italianCities[key]) < val:
            communes.add(key)
    for key in communes:
        del italianCities[key]


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



###### MAIN FUNCTIONS ######


def writeToFile(data, name):
    string = json.dumps(data)
    f = open(name, 'w+')
    f.write(string)
    f.close()

def main(country):
	url = 'https://www.hostelworld.com/hostels/' + country
	cities = buildCityMap(url)
	addPopulationData(country, cities)
	prune(cities, 3)
	addCoordData(cities)
	fileName = country.lower() + 'Data.txt'
	writeToFile(cities, fileName)

def main():
	if len(sys.argv) == 1:
		sys.stderr.write("Please give the country of interest\nProper format is python3 buildHostelList.py ~country~\n")
		return
	url = 'https://www.hostelworld.com/hostels/' + sys.argv[1]
	createList(url)

# Add checks for valid input country
if __name__ == '__main__':
	if len(sys.argv) == 1 or sys.argv[1][0].isLower():
		sys.stderr.write("Please give the country of interest\nProper format is python3 buildCityList.py ~Country~\n")
		return
	maine(sys.argv[1])
















