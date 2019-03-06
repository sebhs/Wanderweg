from screenScrape import Scraper

"""
To-do:
    - Need to add support for countries that aren't organized in the same way on hostelworld
"""

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

# Function to find alternative spellings for a city's name
def findExonyms(url):
    exonyms = []
    scrpr = Scraper(url)
    links = scrpr.search('link')
    first = True
    for link in links:
        if link.get('rel')[0] == 'alternate':
            if first:
                first = False
                continue
            url = link.get('href')
            exo = url.split('/')[-2]
            exonyms.append(exo)
    return exonyms

# Function to build initial map of cities for certain country 
# based off hostelworld.com url of country's base page
def buildCityMap(url, country):
    provences = fetchOtherLocations([url], False)
    print('Starting provences')
    cities = fetchOtherLocations(provences, True)
    print('Finding exonyms')
    cities.sort(key=lambda city: city[0])
    cityMap = {}
    exonyms = {}
    count = 0
    check = .2
    for city in cities:
        count += 1
        if float(count/len(cities)) >= check:
            print('Thru %f of cities' % check)
            check += .2
        cityMap[city[0]] = [country, city[1]]
        exonyms[city[0]] = findExonyms(city[1])
    return cityMap, exonyms
