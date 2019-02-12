"""
Creates list of all trains on goeuro.com for a given city and writes them to file

"""

# Imports
from screenScrape import Scraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from datetime import datetime
from datetime import timedelta
from multiprocessing.pool import ThreadPool
import json
'''
Creates a class that takes two cities as input and finds trips between these two cities
#TODO: Manage a specific date instead of using generic date
'''

class ScrapeCityRoute:

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

		self.tripOptions = None

	def scrapeInfo(self):
		trip_rows = self.driver.find_elements_by_class_name('solutionRow')
		trip_info = []
		for row in trip_rows:
			times = row.find_elements_by_class_name('bottom')
			departTime = times[0].text
			if '*' in departTime: continue		#This is a trip for the next day
			arriveTime = times[1].text
			duration = datetime.strptime(arriveTime, '%H:%M') - datetime.strptime(departTime, '%H:%M')
			duration = duration.total_seconds() / 60
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
		trip_info = self.scrapeInfo()

		# next_page = self.driver.find_elements_by_id('nextPageId')
		# while len(next_page) > 0:
		# 	next_page[0].click()
		# 	trip_info += self.scrapeInfo()
		# 	next_page = self.driver.find_elements_by_id('nextPageId')

		return trip_info

	def findAllInfo(self, cityA='Firenze S. M. Novella', cityB='Venezia S. Lucia', date=None):
		cityA = cityA
		cityB = cityB

		if date == None:
			date = (datetime.now() + timedelta(days=30)).strftime('%d-%m-%Y')

		self.tripOptions = self.findRoutes(cityA, cityB, date)
		fastestOptions = self.findFastest()
		cheapestOptions = self.findCheapest()
		return fastestOptions, cheapestOptions

	def findFastest(self, n=1):
		assert self.tripOptions != None, 'Need to find all info first'
		self.tripOptions.sort(key=lambda x: x[2])
		return self.tripOptions[:n]

	def findCheapest(self, n=1):
		assert self.tripOptions != None, 'Need to find all info first'
		self.tripOptions.sort(key=lambda x: x[3])
		return self.tripOptions[:n]

	def closeWindow(self):
		self.driver.quit()

'''
Class that uses a threadpool to take requests for information from cities and run them in parallel
'''

class RouteData:

	def __init__(self, num_threads=8):
		self.pool = ThreadPool()

	#Takes in a list of [(cityA, cityB, date), ...]
	def getInfo(self, cities):
		self.found_info = []
		self.pool.map(self.processRequest, cities)

	def processRequest(self, trip_inputs):
		cityA, cityB, date = trip_inputs
		print('Processing Request', cityA, cityB, date)
		scraper = ScrapeCityRoute()
		fast, cheap = scraper.findAllInfo()
		fast = fast[0]
		cheap = cheap[0]

	def toJSON(self, cityA, cityB, date, data, result_type, transportation_type):
		json = {'origin': cityA, 'destination': cityB, 'duration': data[2],
				'price': data[3], 'type': result_type, 'transportation': transportation_type}

	def outputInfo(self):
		#TODO: find a way to output JSON info so seb can use
		pass
		
cities = [(None,None,None)]*3
test = RouteData()
test.getInfo(cities)
print(test.found_info)