import urllib.request
from bs4 import BeautifulSoup
import json

'''
Class for gathering climate info on cities. Needs a country and a city 
and then it can find temp mins and maxes, rain, and sun info
'''
class gatherClimate:

    def __init__(self):
        self.url_base = 'https://www.climatestotravel.com/climate/'
        self.url = None
        self.country = None
        self.city = None
        self.soup = None

        self.months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    #Scrapes the appropriate page for the given city and gathers climate data
    def gatherData(self, country='Italy', city='Florence'):
        self.country = country.lower()
        self.city = city.lower()
        self.url = self.url_base + self.country + '/' + self.city

        with urllib.request .urlopen(self.url) as response:
            html = response.read().decode('utf-8')
            self.soup = BeautifulSoup(html, 'html.parser')

        min_temps = self.gatherRow(klass='min-table', filter_term='Fahrenheit')
        max_temps = self.gatherRow(klass='max-table', filter_term='Fahrenheit')
        precip_inches = self.gatherRow(klass='precipit-table', filter_term='inches')[:-1]
        precip_days = self.gatherRow(klass='precipit-table', filter_term='Days')[:-1]
        sunny_hours = self.gatherRow(klass='sole-table')
        print(sunny_hours)

        #TODO: Find a better way to send this back to user? Maybe JSONify?
        return min_temps, max_temps, precip_inches, precip_days, sunny_hours

    #Gathers a single row of climate data
    def gatherRow(self, klass, filter_term=None):
        entries = []
        rows = self.soup.find_all('tr', class_=klass)
        for row in rows:
            if filter_term == None or filter_term in row.th['title']:
                for entry in row.find_all('td'):
                    entries.append(entry.text)
        return entries
        