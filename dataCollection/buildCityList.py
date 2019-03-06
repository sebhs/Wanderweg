"""
Script to build dict of static data on cities in a given country
"""

# Imports
import json
import sys
from hostels import buildCityMap
from population import addPopulationData
from coordinates import addCoordData
from climate import addWeather

# Constants
validCountries = set(["Italy", "France", "Croatia", "Germany"])

def writeToFile(data, filename):
    string = json.dumps(data)
    f = open(filename, 'w+')
    f.write(string)
    f.close()

def main(country):
    url = 'https://www.hostelworld.com/hostels/' + country.lower()
    cities, exonyms = buildCityMap(url, country)
    print("Done with hostelworld scraping")
    addPopulationData(country, cities, exonyms)
    print("Done with population scraping")
    addCoordData(cities)
    print("Done with coordinate scraping")
    addWeather(cities, country, exonyms)
    print("Done with weather scraping")
    citiesFileName = '../database/countries/' + country.lower() + 'Data.txt'
    writeToFile(cities, citiesFileName)
    exosFileName = '../database/exonyms/' + country.lower() + 'Exos.txt'
    writeToFile(exonyms, exosFileName)

# Add checks for valid input country
if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1][0].islower():
        sys.stderr.write("Please give the country of interest\nProper format is python3 buildCityList.py Country\n")
    elif sys.argv[1] not in validCountries:
        sys.stderr.write("That country is currently not supported\n")
    else:
        main(sys.argv[1])