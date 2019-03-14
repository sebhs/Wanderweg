import requests
from bs4 import BeautifulSoup

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
def addWeather(supported_cities, cur_country, exonyms):

    base_url = 'https://en.climate-data.org'
    countries = getCountries(base_url)

    print("Collecting region URLs")
    regions = []
    for country in countries:
        name = country[0]
        url = country[1]
        if name == cur_country:
            regions += getRegions(base_url, url)

    #Check to see if regions are actually cities
    test_url = base_url + regions[0]
    print(test_url)
    # test_response = requests.get(re)

    print("Collecting city URLs")
    cities = []
    for region in regions:
        name = region[0]
        url = region[1]
        cities += getCities(base_url, url)

    weather_cities = {entry[0]:entry[1] for entry in cities}

    print("Scraping supported cities")
    count = 0
    check = .2
    for key in supported_cities:
        count += 1
        if float(count/len(supported_cities)) > check:
            print('Thru %f of cities' % check)
            check += .2
        for city in weather_cities:
            if city == key or city in exonyms[key]:
                city_weather = scrapeCityWeather(base_url, weather_cities[city])
                supported_cities[key].append(city_weather)
                break
        if len(supported_cities[key]) != 6: supported_cities[key].append("No climate data available")
        