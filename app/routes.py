from app import app
from flask import request
import json
from app.climate import GatherClimate
from app.activities import GatherActivities
from app.trains import GatherTrains
from app.population import GatherPop
from pathlib import Path
from db import database as db

@app.route('/')
def home():
    return "Server is running"



#TODO: Modify so it uses city id instead
@app.route('/city_info/<city>')
def getCityInfo(city):
    db_path = str(Path('../Wanderweg/db/sqlite.db').resolve())
    conn = db.create_connection(db_path)
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM city_data WHERE name=?', (city,))
    
    info = cur.fetchall()
    city_info = []
    for entry in info:
        city = {'name': entry[1], 'city_id': entry[0], 'country': entry[2], 'hostel_url': entry[3],
                'population': entry[4], 'latitude': entry[5], 'longitude': entry[6]}
        city_info.append(city)

    return json.dumps(city_info)

'''
Most of this stuff is outdated...we need to make new functions tailored
to exactly what Seb wants.
'''
#Returns climate data for a city. Note that it also requires the country
@app.route('/weather/<country>/<city>')
def getWeather(country, city):
    climateScraper = GatherClimate()
    return climateScraper.scrapeData(country, city)

#Returns activities in a city
@app.route('/activities/<city>')
def getActivities(city):
    activityScraper = GatherActivities()
    return activityScraper.scrapeCity(city)

#Returns train info for a trip between two cities 
#Note that requests need to replace spaces with underscores
@app.route('/trains', methods=['GET'])
def getTrains():
    #Fetch and clean up params
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')
    num_results = int(request.args.get('n'))
    origin = origin.replace("_", " ")
    destination = destination.replace("_", " ")
    #Get route data
    trainScraper = GatherTrains()
    return trainScraper.scrapeAllInfo(origin, destination, date, num_results)

@app.route('/population/<country>/<city>')
def getPopulation(country, city):
    print(country, city)
    popScraper = GatherPop()
    return popScraper.scrapeInfo(country, city)