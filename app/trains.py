from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool
import sys
sys.path.append('../database')
from db_utils import create_connection


base_url = 'https://www.thetrainline.com/book/results?origin=_ORIG_&destination=_DEST_&outwardDate=_DATE_T17%3A45%3A00&outwardDateType=departAfter&journeySearchType=single&passengers%5B%5D=1993-03-05%7C1e63a212-9fa8-4535-b60f-14e457d90166&selectedOutward=f3IZm9oC3Yo%3D%3A0zT3TEdRlg4%3D%3AStandard'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=3')

#Helper function that waits for an element to load 
def waitForLoad(driver, secs, by, val):
	if by == "class": by = By.CLASS_NAME
	elif by == "id": by = By.ID
	elif by == 'xpath': by = By.XPATH

	try:
		WebDriverWait(driver, secs).until(EC.presence_of_element_located((by, val))) 
	except TimeoutException:
		print("Page loaded too slow")
		driver.close()
		driver.quit()

#Helper function that cancels the job if element doesn't load
def cancelLoad(driver, secs, by, val):
	if by == "class": by = By.CLASS_NAME
	elif by == "id": by = By.ID
	elif by == 'xpath': by = By.XPATH

	try:
		WebDriverWait(driver, secs).until(EC.presence_of_element_located((by, val))) 
		return False
	except TimeoutException:
		driver.close()
		driver.quit()
		return True

#Fetch trainline id using the city id we store in our db
def fetchID(sql_id):
	conn = create_connection('../database/wanderweg.db')
	cur = conn.cursor()
	sql = "SELECT trainline_id FROM cities WHERE id = '" + sql_id + "'"
	cur.execute(sql)
	data = cur.fetchone()

	trainline_id = data[0]
	if trainline_id == '0' or trainline_id == 'ID not found':
		trainline_id = None
	return trainline_id

#Scrapes the rows of the page for trip info
def scrapeRows(driver, trip_type='train'):
	route_options = []
	#See if page won't load because there are no routes
	if cancelLoad(driver, 3, 'class', '_dbqts5'):
		return []
	rows = driver.find_elements_by_class_name('_dbqts5')

	#Wait for idividual components to load
	waitForLoad(driver, 3, 'class', '_1rxwtew')
	waitForLoad(driver, 3, 'class', '_1wbkmhm')
	waitForLoad(driver, 3, 'class', '_1xi5pac')
	
	for row in rows:
		opt = {}
		spans = row.find_elements_by_tag_name('span')
		for i, span in enumerate(spans):
			if i == 0: opt['departure_time'] = span.text
			if i == 1: opt['arrival_time'] = span.text
			if i == 4: opt['num_changes'] = span.text
			if i == 7: opt['price'] = span.text

		if 'price' in opt and '$' in opt['price']:
			opt['price'] = opt['price'].replace('$','')
			opt['type'] = trip_type
			duration = (datetime.strptime(opt['arrival_time'], '%H:%M') - datetime.strptime(opt['departure_time'], '%H:%M')).total_seconds()/60
			if duration < 0: duration += 60 * 24
			opt['duration'] = duration
			route_options.append(opt)

	return route_options

#Scrapes for all trip options
def scrapeTrains(origin, destination, date='2019-04-10'):
	orig_id = fetchID(origin)
	dest_id = fetchID(destination)
	if not orig_id or not dest_id:
		print("ID not found for one or more cities")
		return []

	url = base_url.replace('_ORIG_', orig_id).replace('_DEST_', dest_id).replace('_DATE_', date)

	driver = webdriver.Chrome(chrome_options=options)
	driver.get(url)

	#Sleep so page can fully load
	#TODO: Find a better way to do this
	time.sleep(5)

	#Get route options for trains
	route_options = scrapeRows(driver)
			
	# Get route options for busses
	if not cancelLoad(driver, 3, 'class', '_17dn4adNaN'):
		coach_button = driver.find_element_by_class_name('_17dn4adNaN')
		coach_button.click()
		route_options += scrapeRows(driver, trip_type='bus')

	driver.close()
	driver.quit()

	cheapest, fastest, bus = formatOptions(route_options)
	trip_opts = {}
	trip_opts['meta'] = {'orig_id':origin, 'dest_id':destination, 'date':date}
	trip_opts['cheapest'] = cheapest
	trip_opts['fastest'] = fastest
	trip_opts['bus'] = bus

	return trip_opts

def scrapeHelper(input_tuple):
	origin, destination, date = input_tuple
	return scrapeTrains(origin, destination, date)

#Sort options by a few metrics
def formatOptions(trip_options, n=3):
	cost_sort = sorted(trip_options, key=lambda x: (x['type'], -float(x['price'])), reverse=True)
	time_sort = sorted(trip_options, key=lambda x: x['duration'])
	bus_options = []
	for entry in cost_sort:
		if entry['type'] == 'bus': bus_options.append(entry)

	return (cost_sort[:n], time_sort[:n], bus_options[:n])

#Take a list of city_ids and dates and use a threadpool to scrape info for each trip
def scrapeList(trip_list, num_threads=8):
	pool = ThreadPool(num_threads)
	results = pool.map(scrapeHelper, trip_list)
	pool.close()
	pool.join()
	return results

test_list = [('18','21','2019-04-10'), ('53','19','2019-04-10'),
			('21','18','2019-04-10'), ('19','53','2019-04-10'),
			('18','21','2019-04-10'), ('53','19','2019-04-10'),
			('21','18','2019-04-10'), ('19','53','2019-04-10')]
data = scrapeList(test_list)

for entry in data:
	print(entry)








# spans = row.find_elements_by_tag_name('span')
		# i = 0
		# opt = {}
		# #Note for some reason num changes is never attached to the page and breaks everything
		# #TODO: Find a better way to wait for all the spans
		# for span in spans:
		# 	print(trip_type, span.text)
		# 	# if i == 0: opt['departure_time'] = span.text
		# 	# elif i == 1: opt['arrival_time'] = span.text
		# 	# elif i == 3: opt['duration'] = span.text 
		# 	# elif i == 6: opt['cost'] = span.text
		# 	i += 1
		
		# if 'cost' in opt and opt['cost'] != 'Not Available':	
		# 	opt['type'] = trip_type	
		# 	route_options.append(opt)

# waitForLoad(driver, 1, 'xpath', "//div[@class='_16ti7p5']//div[contains(@class,'_1rxwtew')]//span")
		# # time_info = driver.find_element_by_class_name('_1rxwtew ')
		# # spans = row.find_elements_by_xpath("//div[@class='_m3zemr']//div[@class='_1vvi70wy']")
		# spans = row.find_elements_by_xpath("//div[@class='_16ti7p5']//div[contains(@class,'_1rxwtew')]//span")
		# print(len(spans))
		# for i, span in enumerate(spans):
		# 	print(i, span.text)
		
		
		# # print(len(spans))
		# # opt['departure_time'] = spans[0].text
		# # opt['arrival_time'] = spans[1].text

		# # print(opt)






























# '''
# Creates a class that takes two cities as input and finds trips between these two cities
# '''

# class GatherTrains:

# 	def __init__(self, headless=False):
# 		self.headless = headless
# 		#Initialize web driver
# 		options = webdriver.ChromeOptions()
# 		if headless: options.add_argument('headless')		#Use to toggle headless option
# 		self.driver = webdriver.Chrome(chrome_options=options)
# 		self.driver.get('https://www.trenitalia.com/tcom-en')
# 		self.orig_inp = self.driver.find_element_by_id('biglietti_fromNew')
# 		self.dest_inp = self.driver.find_element_by_id('biglietti_toNew')
# 		self.date_inp = self.driver.find_element_by_id('biglietti_data_p')
# 		self.search_button = self.driver.find_element_by_class_name('btn')

# 	def scrapePage(self):
# 		trip_rows = self.driver.find_elements_by_class_name('solutionRow')
# 		trip_info = []
# 		for row in trip_rows:
# 			times = row.find_elements_by_class_name('bottom')
# 			departTime = times[0].text
# 			if '*' in departTime: continue		#This is a trip for the next day
# 			arriveTime = times[1].text
# 			duration = datetime.strptime(arriveTime, '%H:%M') - datetime.strptime(departTime, '%H:%M')
# 			duration = duration.total_seconds() / 60
# 			if duration < 0: duration += 24*60
# 			price = row.find_element_by_class_name('price').text[:-2]

# 			trip_info.append((departTime, arriveTime, duration, price))
# 		return trip_info

# 	def findRoutes(self, orig_text, dest_text, date_text):
# 		self.orig_inp.send_keys(orig_text)
# 		self.dest_inp.send_keys(dest_text)
# 		self.date_inp.clear()
# 		self.date_inp.send_keys(date_text)	
# 		self.search_button.click()

# 		#Get trip depart time, arrival time, and price
# 		trip_info = self.scrapePage()

# 		next_page = self.driver.find_elements_by_id('nextPageId')
# 		while len(next_page) > 0:
# 			next_page[0].click()
# 			trip_info += self.scrapePage()
# 			next_page = self.driver.find_elements_by_id('nextPageId')

# 		return trip_info

# 	def scrapeAllInfo(self, cityA='Firenze S. M. Novella', cityB='Venezia S. Lucia', date=None, n=1):
# 		cityA = cityA
# 		cityB = cityB

# 		if date == None:
# 			date = (datetime.now() + timedelta(days=30)).strftime('%d-%m-%Y')

# 		self.tripOptions = self.findRoutes(cityA, cityB, date)
# 		fastestOptions = self.findFastest(n)
# 		cheapestOptions = self.findCheapest(n)

# 		#Create json object
# 		options_json = {"origin": cityA, "destination": cityB, "date":date, "fastest": fastestOptions,
# 						"cheapest":cheapestOptions, "type":"train"}

# 		self.driver.quit()
# 		return json.dumps(options_json)

# 	def findFastest(self, n):
# 		self.tripOptions.sort(key=lambda x: x[2])
# 		return self.tripOptions[:n]

# 	def findCheapest(self, n):
# 		self.tripOptions.sort(key=lambda x: x[3])
# 		return self.tripOptions[:n]
