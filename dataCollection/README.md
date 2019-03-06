# Overview:
    - This folder is for files that gather static data that we load into our database.
    - Data is primarily gathered by scraping websites, but some data is collected through API queries

# Files:
    - buildCityList.py: 
      Builds a list of data for each city we support in Wanderweg. This data 
      lives in ../database/countries/<country>Data.txt and contains city specific info such as population and weather.

    - climate.py:
      Functions to gather climate data for a list of cities

    - coordinates.py:
      Functions to gather coordinates for a list of cities

    - hostels.py:
      Functions to get the names of all the cities with hostels inside a given country as well as the url for that city on hostelworld.com 

    - population.py:
      Functions to get population data for a list of cities

    - screenScrape.py: 
      Utility file to aide scraping data from websites

# Data Collection Files
Per country static data generation

# Interesting challenges
- Server's with checks for Python based bots/crawlers
  - Adding certain headers to the request allows us to evade
- English exonyms vs local toponyms
  - Pre-exonym use: population hit rate of 70.5% (Italy) and 61.5% (France)
  - Post-exonym use: population hit rate of 72.1% (Italy) and 64.1% (France)
  - Turns out the bigger problem with population was that most of the cities I wasn't finding were smaller than 15,000 which was the lower limit on the list of cities I was working with

# Notes:
    - buildCityList.py should only need to be run once per country. Avoid running too much, as we have limited daily queries
