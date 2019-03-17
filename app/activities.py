import requests
from bs4 import BeautifulSoup
import json

class GatherActivities:

    def __init__(self):
        self.url = "https://developers.musement.com/api/v3/activities"

    def scrapeCity(self, city, coords):
        latitude, longitude = coords
        query_params = {"text":city, "sort_by":"price","coordinates":str(latitude)+','+str(longitude)}
        response = requests.request("GET", self.url, params=query_params)
        self.json = response.json()

        #All the relevant data is kept in self.json['data']

        #Filter to only the city we care about
        filtered_activities = {}
        filtered_activities['meta'] = self.json['meta']
        filtered_activities['data'] = []
        for activity in self.json['data']:
            cur_city = activity['city']['name']
            if cur_city == city:
                filtered_activities['data'].append(activity)
        
        return json.dumps(filtered_activities)