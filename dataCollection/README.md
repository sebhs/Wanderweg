# Overview:
    - This folder is for files that gather static data that we load into our database.
    - Data is primarily gathered by scraping websites, but some data is collected through API queries
    -  

# Files:
    - activities.py:
      Doesn't gather static data, move to app

    - buildCityList.py: 
      Builds a list of data for each city we support in Wanderweg. This data 
      lives in ../database/countries/<country>Data.txt and contains city specific info such as population and weather.
    
    - climate.py: 
      Uses weatherbase_cities .csv to build a database table of all cities we can get weather for, then 
      adds scrapes for weather information on cities we are supporting in Wanderweg. Data is added to the database table 
      city_features in ../database/sqlite.db
    
    - screenScrape.py: 
      Utility file to aide scraping data from websites

# Data Collection Files
Per country static data generation

# Interesting challenges
- Server's with checks for Python based bots/crawlers
- English exonyms vs local toponyms

# Notes:
    - buildCityList.py should only need to be run once per country. Avoid running too much, as we have limited daily queries
