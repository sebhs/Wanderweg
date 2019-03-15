
# Imports
from app import app
from flask import request
import flask
from datetime import datetime, timedelta
import sys
import json
sys.path.append('./database')
sys.path.append('./app')
from db_utils import create_connection
from activities import GatherActivities
from hostels import gatherHostelData
import trains

@app.route('/')
def home():
    return "Server is running"


@app.route('/cities')
def getCitiesOverview():

    # Database query
    conn = create_connection('./database/wanderweg.db')
    cur = conn.cursor()
    sql = 'SELECT id,name,country,population,latitude,longitude,trainline_id FROM cities'
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()

    # Format response
    cities = []
    for entry in data:
        if entry[-1] != '0' and entry[-1] != 'ID not found':
            city = {'name': entry[1], 'city_id': entry[0], 'country': entry[2], 'population': entry[3], 'location': {'lat': entry[4], 'lng': entry[5]}}
            cities.append(city)
    
    response = flask.jsonify(cities)
    return response


@app.route('/city_info/<cid>')
def getCityInfo(cid):
    
    # Database query
    conn = create_connection('./database/wanderweg.db')
    cur = conn.cursor()
    sql = 'SELECT name,country,hostel_url,population,weather,hostelworld_pic,latitude,longitude FROM cities WHERE id=' + cid
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()

    if not data:
        info = {'error': 'no country with that ID found'}
        response = flask.jsonify(info)
        return response
        
    # Fetch activities
    activityScraper = GatherActivities()
    #Use latitude and longitude to refine activity gathering
    activities = activityScraper.scrapeCity(data[0], (data[-2], data[-1]))
   
    # Fetch hostel info
    hostelData = gatherHostelData(data[2])

    # Format response
    info = {'city_id': int(cid), 'population': data[3], 'name': data[0], 'country': data[1], 
            'activities': activities, 'hostels': hostelData, 'weather': data[4], 'alt_cover': data[5]}
    response = flask.jsonify(info)
    return response


# Use params or something to accept a list of destinations
@app.route('/route_info', methods=['POST'])
def createTravelPlan():  
    #Extract info from post request
    info = json.loads(request.data)
    trip_info = info['trip_info']
    city_pairs = []
    dates = []
    for i, entry in enumerate(trip_info):
        if i < len(trip_info) - 1 : city_pairs.append((trip_info[i]['city_id'], trip_info[i+1]['city_id']))
        if i > 0: dates.append(entry['ISO_date'])
    
    #Format into list of route requests
    request_list = []
    for i in range(len(city_pairs)):
        origin = city_pairs[i][0]
        destination = city_pairs[i][1]
        date = dates[i].split('T')[0]
        formatted_tuple = (str(origin), str(destination), date)
        request_list.append(formatted_tuple)

    #Fetch route options using trains.py
    route_options = trains.scrapeList(request_list)
    response = flask.jsonify(route_options)
    print(response.data)
    return response