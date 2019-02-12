import requests
from bs4 import BeautifulSoup
import json

class ActivityScraper:

    def __init__(self):
        self.url = "https://developers.musement.com/api/v3/activities"

    def scrapeCity(self, city):
        query_params = {"text":city, "sort_by":"price"}
        response = requests.request("GET", self.url, params=query_params)
        self.json = response.json()

        #All the relevant data is kept in self.json['data']
