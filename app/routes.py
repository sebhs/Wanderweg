
# Imports
from app import app
from flask import request
import json
import sys
sys.path.append('./database')
from db_utils import create_connection

# Potentially useful imports:
#from app.activities import GatherActivities
#from app.trains import GatherTrains

@app.route('/')
def home():
    return "Server is running"

#TODO: Do we want this to just return id, name, and population? Would speed up 
#query and my understanding is that this is just to get city ids for later queries
@app.route('/cities')
def getCitiesOverview():

    # Database query
    conn = create_connection('./database/Wanderweg.db')
    cur = conn.cursor()
    sql = 'SELECT id,name,country,population,latitude,longitude FROM cities'
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()

    # Format response
    cities = []
    for entry in data:
        city = {'name': entry[1], 'city_id': entry[0], 'country': entry[2], 'population': entry[3], 
                'latitude': entry[4], 'longitude': entry[5]}
        cities.append(city)

    return json.dumps(cities)


@app.route('/city_info/<cid>')
def getCityInfo(cid):
    # Database query

    conn = create_connection('./database/Wanderweg.db')
    cur = conn.cursor()
    sql = 'SELECT name,country,hostel_url,weather FROM cities WHERE id=' + cid
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()

    # TODO: Scrape hostelworld
    # TODO: Fetch activities

    return "The city corresponding to id #" + cid + " is: " + data[0] + ", " + data[1] + \
            " with weather " + data[3]


# Use params or something to accept a list of destinations
@app.route('/travel', methods=['GET'])
def createTravelPlan():
    return "TODO"

"""
Saved these two routes because they could be usefull for helper function for our final routes.
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

"""