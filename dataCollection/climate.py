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

def hasRegions(soup):
    headers = soup.find_all('h2')
    for h in headers:
        if h.text.lower() == 'regions': return True
    return False

#Helper function to get all regions
def getRegions(base_url, country_base_url):
    country_url = base_url + country_base_url
    response = requests.get(country_url, 'html5lib')
    soup = BeautifulSoup(response.content, 'html5lib')
    if not hasRegions(soup): return [('idk', country_base_url, True)]
    article = soup.find('div', id='article')
    regions_li = article.find_all('li')
    regions = []
    for region_li in regions_li:
        link = region_li.find('a')
        regions.append((link.text, link['href'], False))
    return regions

def invalidLink(link):
    if '#example' in link['href']: return True
    if './?page=' in link['href']: return True
    if '#temperature-graph' in link['href']: return True
    if '#climate-graph' in link['href']: return True
    if 'name' in link.attrs: return True
    if len(link.contents) == 1: return True
    return False

# Helper function to get all cities
def getCities(base_url, region_base_url, country, page=''):
    region_url = base_url + region_base_url + page
    response = requests.get(region_url, 'html5lib')
    soup = BeautifulSoup(response.content, 'html5lib')
    data = soup.find('div', id='article')
    link_elems = data.find_all('a')
    cities = []
    for link_elem in link_elems:
        if country:
            if invalidLink(link_elem): continue
            link = link_elem['href']
            name = link_elem.find('span', class_='name').text
            cities.append((name, link))
        else:
            link = link_elem['href']
            name = link_elem.find('span', class_='name').text
            cities.append((name, link))
    
    pages = soup.find('div', class_='pagination')
    page_links = pages.find_all('a')
    last_link = page_links[-1]
    if last_link.text == 'Next':
        next_page_url = last_link['href']
        next_page_url = next_page_url[2:]
        cities += getCities(base_url, region_base_url, country, page=next_page_url)
    
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

def inExonyms(names, exos):
    for name in names: 
        if name in exos: return True
    return False


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
    
    print("Collecting city URLs")
    cities = []
    for region in regions:
        name = region[0]
        url = region[1]
        cities += getCities(base_url, url, region[2])

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
            names = city.split('/')
            if key in names or inExonyms(names, exonyms[key]):
                city_weather = scrapeCityWeather(base_url, weather_cities[city])
                supported_cities[key].append(city_weather)
                break
        if len(supported_cities[key]) < 7: supported_cities[key].append("No climate data available")
