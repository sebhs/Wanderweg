import re
from screenScrape import Scraper

# Finds the name of the city
def getName(scrpr):
    search = scrpr.search('span', klass='city-name')
    regex = '[a-zA-Z.]+(?:[ -][a-zA-Z]+)*'
    words = re.findall(regex, search[0].text)
    return words[0]

# Returns if the url is for a city page or not
def isCityPage(scrpr):
    check = scrpr.search('div', klass='frcx-banner')
    check2 = scrpr.search('section', klass='fab-usp')
    return len(check) and len(check2)

# Scrapes the header image from any hostelworld page
def getHeaderImage(scrpr):
    options = scrpr.search('div', klass='coverback', portion='data-interchange')
    if not options: return ''
    options = re.sub("\n +","", options[0])
    options = options[1:-1]
    options = options.split('],[')
    [url, typ] = options[0].split(', ')
    url = 'https:' + url
    return url

# Function to find provence and city URLs / names
def fetchOtherLocations(scrpr):
        container = scrpr.search('div', klass='otherlocations')
        return(scrpr.search('a', portion='href', html=container[0]))

# Function to find alternative spellings for a city's name
def findExonyms(scrpr):
    exonyms = []
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
    cityMap = {}
    exonyms = {}
    urls = [url]
    while urls:
        url = urls.pop()
        s = Scraper(url)
        if isCityPage(s):
            name = getName(s)
            cityMap[name] = [country, url, getHeaderImage(s)]
            exonyms[name] = findExonyms(s)
        else:
            urls.extend(fetchOtherLocations(s))
    return cityMap, exonyms















