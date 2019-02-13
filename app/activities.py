import requests
from bs4 import BeautifulSoup
import json

class GatherActivities:

    def __init__(self):
        self.url = "https://developers.musement.com/api/v3/activities"

    def scrapeCity(self, city):
        query_params = {"text":city, "sort_by":"price"}
        response = requests.request("GET", self.url, params=query_params)
        self.json = response.json()

        #All the relevant data is kept in self.json['data']

        #Filter to only info we care about
        #TODO: Add more relevant info, make sure prices are in dollars
        all_activities = {'city':city, 'data':[]}
        for activity in self.json['data']:
            if 'description' not in activity: continue
            activity_info = {}
            activity_info['title'] = activity['title']
            activity_info['description'] = activity['description']
            activity_info['about'] = activity['about']
            activity_info['price'] = activity['retail_price']['value']
            activity_info['review_count'] = activity['reviews_number']
            activity_info['ave_review'] = activity['reviews_avg']
            if 'latitude' in activity: activity_info['latitude'] = activity['latitude']
            if 'longitude' in activity: activity_info['longitude'] = activity['longitude']

            all_activities['data'].append(activity_info)

        # return json.dumps(all_activities)
        return json.dumps(self.json)