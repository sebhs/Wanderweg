from screenScrape import Scraper

# Function to add the population data for each city to the city map
def addPopulationData(country, cityMap, exonyms):
    url = 'https://population.mongabay.com/population/' + country.lower() + '/'
    s = Scraper(url)
    rows = s.search('tr')
    for row in rows:
        [link, pop] = s.search('td', html=row)
        city = link.find('a').text
        for key in cityMap:
            if city == key or city in exonyms[key]:
                cityMap[key].append(int(pop.text.replace(',', '')))
                break
    
    for key in cityMap:
        if len(cityMap[key]) < 4:
            cityMap[key].append(0)