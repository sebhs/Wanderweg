
# Imports
from app import app
from flask import request
import flask
import sys
sys.path.append('./database')
from db_utils import create_connection
sys.path.append('./app')
from activities import GatherActivities
from hostels import gatherHostelData

# Potentially useful imports:
#from app.trains import GatherTrains

@app.route('/')
def home():
    return "Server is running"


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
        city = {'name': entry[1], 'city_id': entry[0], 'country': entry[2], 'population': entry[3], 'location': {'lat': entry[4], 'lng': entry[5]}}
        cities.append(city)
    
    response = flask.jsonify(cities)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/city_info/<cid>')
def getCityInfo(cid):
    
    # Database query
    conn = create_connection('./database/Wanderweg.db')
    cur = conn.cursor()
    sql = 'SELECT name,country,hostel_url,population,weather FROM cities WHERE id=' + cid
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()

    if not data:
        info = {'error': 'no country with that ID found'}
        response = flask.jsonify(info)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    # Fetch activities
    # TO DO: should we include country in acitivities search? Could help for when we scale
    activityScraper = GatherActivities()
    activities = activityScraper.scrapeCity(data[0])
   
    # Fetch hostel info
    hostelData = gatherHostelData(data[2])

    # Format response
    info = {'city_id': int(cid), 'population': data[3], 'name': data[0], 'country': data[1], 
            'activities': activities, 'hostels': hostelData, 'weather': data[4]}
    response = flask.jsonify(info)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Use params or something to accept a list of destinations
@app.route('/travel', methods=['GET'])
def createTravelPlan():
    return "TODO"
