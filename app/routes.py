
# Imports
from app import app
from flask import request
import flask
from datetime import datetime, timedelta
import sys
sys.path.append('./database')
sys.path.append('./app')
from db_utils import create_connection
from activities import GatherActivities
from hostels import gatherHostelData
import trains

# Potentially useful imports:
#from app.trains import GatherTrains

@app.route('/')
def home():
    return "Server is running"


@app.route('/cities')
def getCitiesOverview():

    # Database query
    conn = create_connection('./database/wanderweg.db')
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
    conn = create_connection('./database/wanderweg.db')
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
@app.route('/route_info', methods=['POST'])
def createTravelPlan():
    #Extract info from post request
    trip_info = request.form['trip_info']
    city_pairs = []
    dates = []
    for i, entry in enumerate(trip_info):
        if i < len(trip_info) : city_pairs.append((trip_info[i]['city_id'], trip_info[i+1]['city_id']))
        if i > 0: dates.append(entry['ISO_date'])
    
    #Format into list of route requests
    request_list = []
    for i in range(len(city_pairs)):
        origin = city_pairs[i][0]
        destination = city_pairs[i][1]
        date = datetime.strptime(dates[i], "%Y-%m-%dT%H:%M:%S%z")
        date = datetime.strftime(date, '%Y-%m-%d')
        formatted_tuple = (origin, destination, date)
        request_list.append(formatted_tuple)

    #Fetch route options using trains.py
    route_options = trains.scrapeList(request_list)
    return flask.jsonify(route_options)