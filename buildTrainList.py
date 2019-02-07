"""
Creates list of all trains on goeuro.com for a given city and writes them to file

TODO:
	- Add multiprocessing (threadpool?) to speed up
"""

# Imports
from screenScrape import Scraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

# Grab input elements from trenitalia
# def initInputs(driver):
# 	driver.get('https://www.trenitalia.com/tcom-en')
# 	origin = driver.find_element_by_id('biglietti_fromNew')
# 	dest = driver.find_element_by_id('biglietti_toNew')
# 	date = driver.find_element_by_id('biglietti_data_p')
# 	search = driver.find_element_by_class_name('btn')
# 	return origin, dest, date, search

# Grab input elements from raileurope
def initInputs(driver):
	driver.get('https://www.raileurope.com/')
	origin = driver.find_element_by_class_name('js-reverser-left')
	print(origin)
	# locs = driver.find_element_by_css_selector("[data-id='departurePostion']")
	# print(locs)
	# origin = driver.find_element_by_id('biglietti_fromNew')
	# dest = driver.find_element_by_id('biglietti_toNew')
	# date = driver.find_element_by_id('biglietti_data_p')
	# search = driver.find_element_by_class_name('btn')
	# return origin, dest, date, search

def scrapeInfo(driver):
	trip_rows = driver.find_elements_by_class_name('solutionRow')
	trip_info = []
	for row in trip_rows:
		times = row.find_elements_by_class_name('bottom')
		departTime = times[0].text
		if '*' in departTime: continue		#This is a trip for the next day
		arriveTime = times[1].text
		price = row.find_element_by_class_name('price').text[:-2]

		trip_info.append((departTime, arriveTime, price))
	return trip_info

def sendCities(driver, orig_inp, dest_inp, depart_inp, search, orig_text, dest_text, date):
	orig_inp.send_keys(orig_text)
	dest_inp.send_keys(dest_text)
	depart_inp.clear()
	depart_inp.send_keys(date)	#TODO: How do we select the ideal date(s)?
	search.click()

	#Get trip depart time, arrival time, and price
	trip_info = scrapeInfo(driver)

	next_page = driver.find_elements_by_id('nextPageId')
	while len(next_page) > 0:
		next_page[0].click()
		trip_info += scrapeInfo(driver)
		next_page = driver.find_elements_by_id('nextPageId')

	print(trip_info)
	
	input("Press Enter to continue...")

def main():
	
	#TODO: Use a ThreadPool to run multiple headless drivers at once
	options = webdriver.ChromeOptions()
	# options.add_argument('headless')		#Use to toggle headless option
	driver = webdriver.Chrome(chrome_options=options)
	cities = [('Firenze ( Tutte Le Stazioni )', 'Venezia ( Tutte Le Stazioni )')]
	# cities = [('Firenze ( Tutte Le Stazioni )', 'Venezia ( Tutte Le Stazioni )')]

	for city in cities:
		a,b = city
		date = '08-02-2019'
		orig_inp, dest_inp, date_in, search = initInputs(driver)
		sendCities(driver, orig_inp, dest_inp, date_in, search, a, b, date)


if __name__ == '__main__':
	main()
