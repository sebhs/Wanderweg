# Overview:
    - This folder holds files that support the flask server
    - The server itself is run through ../api.py, but supporting files live here
    - Files in this folder exist primarily to gather dynamic data by scraping or
      accessing an API

# Files:
    - activites.py: 
      Uses activites api to query for activity data for a specific city
    
    - routes.py:
      Holds all the server endpoints. Uses database queries and other files within app to satisfy requests

    - screenScrape.py:
      Utility file for scraping, should live in dataCollection

    - trains.py:
      Scrapes for information on train routes between cities

# Server Info


### How to run server
1. Change to Wanderweg directory
2. Enter "pip3 install flask" in the command line
3. Enter "flask run" in the command line
4. Install any dependencies it recommends


### Questions
- Should we always be defining the routes with the methods that are allowed to call them?
    - ^ what does this mean

