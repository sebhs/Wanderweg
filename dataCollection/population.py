# http://worldpopulationreview.com/world-cities/milan-population/
# http://worldpopulationreview.com/world-cities/

# https://en.wikipedia.org/wiki/<city>

import urllib.request
import requests
from bs4 import BeautifulSoup
import json

'''
Class for gathering city population. Takes a city name and county and returns city population
as found on Wikipedia. Currently only works for Italy.
'''

class GatherPop:

    def __init__(self):
        self.italy_url = "https://en.wikipedia.org/wiki/List_of_cities_in_Italy"

    def scrapeInfo(self, country, city):
        if country == 'Italy': return self.scrapeItaly(city)
        
    def scrapeItaly(self, city):
        with urllib.request.urlopen(self.italy_url) as response:
            html = response.read().decode('utf-8')
            self.soup = BeautifulSoup(html, 'html.parser')

        table = self.soup.find(True, {'class':['wikitable','sortable', 'jquery-tablesorter']})
        table = table.find('tbody')
        rows = table.findAll('tr')
        
        ans = {}
        for row in rows[1:]:
            cells = row.findAll('td')
            cur_city = cells[1].text
            if cur_city == city:
                pop = int(cells[3].text.replace(',',''))
                ans = {cur_city: pop}

        return json.dumps(ans)
        
test = GatherPop()
test.scrapeInfo('Italy', 'Milan')

# def __init__(self):
    #     self.url = 'https://query.wikidata.org/sparql'
    #     self.query = """
    #     SELECT DISTINCT ?country ?population ?area ?cityL ?countryL
    #     WHERE
    #     {
    #         ?city   wdt:P31/wdt:P279* wd:Q515;
    #                 wdt:P17 ?country;
    #                 wdt:P1082 ?population;
    #                 rdfs:label ?cityL.
    #         #?country rdfs:label ?countryL.
    #         OPTIONAL { ?city   wdt:P2046    ?area. }
    #         FILTER(CONTAINS(?cityL, "CITYTEMP"))
    #         SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }

            
    #     }
    #     """

    #     # ?country rdfs:label ?countryL.
    #     #     FILTER(CONTAINS(?countryL, "Italy"))


    #     #?country rdfs:label ?countryL.
    #         #FILTER(CONTAINS(?countryL, "Italy")).
    #         #SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }


    # def scrapeInfo(self, city):
    #     self.query = self.query.replace('CITYTEMP', city)
    #     r = requests.get(self.url, params = {'format': 'json', 'query': self.query})
    #     data = r.json()

    #     for item in data['results']['bindings']:
    #         print(item)
    #         # if "ita" in item['countryL']['value']:
    #         #     print(item['countryL']['value'])
    #         # print(item['countryL']['value'])

    #     print(len(data['results']['bindings']))








#         #Get page html
#         url = self.url_base + city
#         with urllib.request.urlopen(url) as response:
#             html = response.read().decode('utf-8')
#             soup = BeautifulSoup(html, 'html.parser')

#         table = soup.find(True, {'class':['infobox','geography','vcard']})
#         rows = table.find_all('tr', class_='mergedtoprow')
#         info = []
#         for row in rows:
#             head = row.find('th')
#             if head and ('Population' in head.text or 'Area' in head.text):
#                 for sib in row.next_siblings:
#                     # print(sib.text)
#                     if sib.has_attr('class') and sib['class'][0] == 'mergedtoprow':
#                         info.append(sib.previous_sibling.text)
#                         break      
                 
#         print(info)
            
#             # content = row.find('td')
#             # if head:
#             #     if not content: content = "none"
#             #     else: content = content.text
#             #     print(head.text, content)
            
#             # td = row.find('td')
#             # if 'sq' in td.text or len(info) == 1:
#             #     info.append(td.text)

#         #Clean to get definative area and population
#         # info = info[:2]
#         # area = info[0].split(' ')[1][1:-1].replace('\xa0sq\xa0mi', '')
#         # population = info[1]
#         # print(area, population)

# test = GatherPop()
# test.scrapeInfo('Florence')