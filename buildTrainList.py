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

def initInputs(driver):
	driver.get('https://www.trenitalia.com/tcom-en')
	origin = driver.find_element_by_id('biglietti_fromNew')
	dest = driver.find_element_by_id('biglietti_toNew')
	date = driver.find_element_by_id('biglietti_data_p')
	search = driver.find_element_by_class_name('btn')
	return origin, dest, date, search

def sendCities(orig_inp, dest_inp, depart_inp, search, orig_text, dest_text, date):
	orig_inp.send_keys(orig_text)
	dest_inp.send_keys(dest_text)
	depart_inp.clear()
	depart_inp.send_keys(date)	#TODO: How do we select the ideal date(s)?
	search.click()

	#TODO: Actually scrape price info

	input("Press Enter to continue...")

def main():
	options = webdriver.ChromeOptions()
	# options.add_argument('headless')		#Use to toggle headless option
	driver = webdriver.Chrome(chrome_options=options)
	cities = [('Firenze S. M. Novella', 'Venezia S. Lucia')]

	for city in cities:
		a,b = city
		date = '07-02-2019'
		orig_inp, dest_inp, date_in, search = initInputs(driver)
		sendCities(orig_inp, dest_inp, date_in, search, a, b, date)

if __name__ == '__main__':
	main()
