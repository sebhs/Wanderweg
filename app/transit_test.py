from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# import requests
# import json
# import trainline
import time


base_url = 'https://www.thetrainline.com/'

options = webdriver.ChromeOptions()
# options.add_argument('headless')

#TODO: Add date
def scrapeTrains(origin, destination, date=None):
	driver = webdriver.Chrome(chrome_options=options)
	driver.get(base_url)

	#Navigate to page to input origin and destination
	inputs = driver.find_elements_by_class_name('_b2dtf3NaN')
	orig_inp = inputs[0]
	dest_inp = inputs[1]
	date_inp = driver.find_element_by_class_name('_vb9840NaN')
	search = driver.find_element_by_class_name('_1tuqvrz4')

	#TODO: Find out how to select the optimal element from the dropdown
	orig_inp.send_keys(origin)
	orig_inp.send_keys(Keys.ARROW_DOWN)
	orig_inp.send_keys(Keys.RETURN)

	dest_inp.send_keys(destination)
	dest_inp.send_keys(Keys.ARROW_DOWN)
	dest_inp.send_keys(Keys.RETURN)

	if date: 
		date_inp.send_keys(Keys.CONTROL + 'a')
		date_inp.send_keys(Keys.DELETE)
		date_inp.send_keys(date)
		date_inp.send_keys(Keys.ENTER)

	time.sleep(.5)
	search.click()
	time.sleep(10)

	#Scrape price info
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_dbqts5'))) 
	except TimeoutException:
		print("Page loaded too slow")
		driver.close()
		driver.quit()

	#Price info for trains
	rows = driver.find_elements_by_class_name('_dbqts5')
	trip_options = []
	for row in rows:
		elems = row.find_elements_by_tag_name('span')
		trip_info = {'type':'train'}
		i = 0
		for elem in elems:
			if elem.text:
				if i == 0: trip_info['departure_time'] = elem.text
				if i == 1: trip_info['arrival_time'] = elem.text
				if i == 2: trip_info['duration'] = elem.text
				if i == 4: trip_info['num_changes'] = elem.text
				if i == 5: trip_info['standard_price'] = elem.text
				i += 1
		if 'standard_price' in trip_info and 'available' not in trip_info['standard_price']: 
			trip_options.append(trip_info)

	#Price info for busses
	#TODO: Finish this
	bus_toggle = driver.find_elements_by_class_name('_1u112skNaN')
	if len(bus_toggle) > 0:
		bus_toggle = bus_toggle[0]
		bus_toggle.click()


	driver.close()
	driver.quit()

	return trip_options

trip_info = scrapeTrains('Paris', 'Rome', '15-Mar-19')
print(trip_info)









# -*- coding: utf-8 -*-
# import trainline

# results = trainline.search(
# 	departure_station="Firenze",
# 	arrival_station="Bordeaux",
# 	from_date="15/10/2018 08:00",
# 	to_date="15/10/2018 21:00")

# print(results.csv())



# import trainline

# results = trainline.search(
# 	departure_station="Firenze",
# 	arrival_station="Roma",
# 	from_date="15/10/2019 08:00",
# 	to_date="15/10/2019 21:00")

# print(results.csv())









# options = webdriver.ChromeOptions()
# if True: options.add_argument('headless')

# driver = webdriver.Chrome(chrome_options=options)
# self.driver.get('https')

# base_url = 'https://www.thetrainline.com/buytickets/'
# predata = {'OriginStation':'Stockport',
# 'DestinationStation':'firenze',
# 'RouteRestriction':'NULL',
# 'ViaAvoidStation':'',
# 'journeyTypeGroup':'return',
# 'outwardDate':'14-Apr-19',
# 'OutwardLeaveAfterOrBefore':'A',
# 'OutwardHour':'15',
# 'OutwardMinute':'15',
# 'returnDate':'16-Apr-19',
# 'InwardLeaveAfterOrBefore':'A',
# 'ReturnHour':'9',
# 'ReturnMinute':'0',
# 'AdultsTravelling':'1',
# 'ChildrenTravelling':'0',
# 'railCardsType_0':'YNG',
# 'railCardNumber_0':'1',
# 'ExtendedSearch':'Get times & tickets'
# }

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# response = requests.post(base_url, headers=headers, data=predata)
# soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())
# all_rows = soup.find_all('div', class_='_dbqts5')
# useful_rows = []
# for row in all_rows:
#     print(row)
#     if 'data-test' in row.attrs:
#         useful_rows.append(row)

# print(useful_rows)






# key = 'AIzaSyBmNI8Q0_efb8UzwvnDej0n7uYcLj8G2x8'

# base_url = 'https://maps.googleapis.com/maps/api/directions/json'

# params = {'origin':'Florence', 'destination':'Rome', 'key':key,
#             'mode':'transit','alternatives':False, 'language':'en',
#             'units':'imperial', 'transit_mode':'train'}

# response = requests.get(base_url, params=params)
# j = response.json()
# for key in j.keys():
#     for entry in j[key]:
#         print(entry)