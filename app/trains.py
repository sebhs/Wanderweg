"""
Creates list of all trains on goeuro.com for a given city and writes them to file
"""

# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from datetime import datetime
from datetime import timedelta
from multiprocessing.pool import ThreadPool
import json

'''
Creates a class that takes two cities as input and finds trips between these two cities
'''

class GatherTrains:

	def __init__(self, headless=False):
		self.headless = headless
		#Initialize web driver
		options = webdriver.ChromeOptions()
		if headless: options.add_argument('headless')		#Use to toggle headless option
		self.driver = webdriver.Chrome(chrome_options=options)
		self.driver.get('https://www.trenitalia.com/tcom-en')
		self.orig_inp = self.driver.find_element_by_id('biglietti_fromNew')
		self.dest_inp = self.driver.find_element_by_id('biglietti_toNew')
		self.date_inp = self.driver.find_element_by_id('biglietti_data_p')
		self.search_button = self.driver.find_element_by_class_name('btn')

	def scrapePage(self):
		trip_rows = self.driver.find_elements_by_class_name('solutionRow')
		trip_info = []
		for row in trip_rows:
			times = row.find_elements_by_class_name('bottom')
			departTime = times[0].text
			if '*' in departTime: continue		#This is a trip for the next day
			arriveTime = times[1].text
			duration = datetime.strptime(arriveTime, '%H:%M') - datetime.strptime(departTime, '%H:%M')
			duration = duration.total_seconds() / 60
			if duration < 0: duration += 24*60
			price = row.find_element_by_class_name('price').text[:-2]

			trip_info.append((departTime, arriveTime, duration, price))
		return trip_info

	def findRoutes(self, orig_text, dest_text, date_text):
		self.orig_inp.send_keys(orig_text)
		self.dest_inp.send_keys(dest_text)
		self.date_inp.clear()
		self.date_inp.send_keys(date_text)	
		self.search_button.click()

		#Get trip depart time, arrival time, and price
		trip_info = self.scrapePage()

		next_page = self.driver.find_elements_by_id('nextPageId')
		while len(next_page) > 0:
			next_page[0].click()
			trip_info += self.scrapePage()
			next_page = self.driver.find_elements_by_id('nextPageId')

		return trip_info

	def scrapeAllInfo(self, cityA='Firenze S. M. Novella', cityB='Venezia S. Lucia', date=None, n=1):
		cityA = cityA
		cityB = cityB

		if date == None:
			date = (datetime.now() + timedelta(days=30)).strftime('%d-%m-%Y')

		self.tripOptions = self.findRoutes(cityA, cityB, date)
		fastestOptions = self.findFastest(n)
		cheapestOptions = self.findCheapest(n)

		#Create json object
		options_json = {"origin": cityA, "destination": cityB, "date":date, "fastest": fastestOptions,
						"cheapest":cheapestOptions, "type":"train"}

		self.driver.quit()
		return json.dumps(options_json)

	def findFastest(self, n):
		self.tripOptions.sort(key=lambda x: x[2])
		return self.tripOptions[:n]

	def findCheapest(self, n):
		self.tripOptions.sort(key=lambda x: x[3])
		return self.tripOptions[:n]
