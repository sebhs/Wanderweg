from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from multiprocessing.pool import ThreadPool
from unidecode import unidecode
import random
import json
import sys
import time
sys.path.append('../database')
from db_utils import create_connection


#Helper function that waits for an element to load 
def waitForLoad(driver, secs, by, val):
	if by == "class": by = By.CLASS_NAME
	elif by == "id": by = By.ID

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

	try:
		WebDriverWait(driver, secs).until(EC.presence_of_element_located((by, val))) 
		return False
	except TimeoutException:
		print("Page loaded too slow, load canceled")
		driver.close()
		driver.quit()
		return True

def scrapeIDs(origin, destination):
	driver = webdriver.Chrome(chrome_options=options)
	driver.get(base_url)

	#Navigate to page to input origin and destination
	waitForLoad(driver, 5, 'class', '_b2dtf3NaN')
	inputs = driver.find_elements_by_class_name('_b2dtf3NaN')
	orig_inp = inputs[0]
	dest_inp = inputs[1]

	#Select the desired location from the dropdown for origin and destination
	if origin[0] == origin[2]:
		orig_inp.send_keys(origin[0])
	else: 
		orig_inp.send_keys(origin[1])
	if cancelLoad(driver, 5, 'id', 'stations_from'):
		return {origin[2]:"One city in pair could not be found", destination[2]:"One city in pair could not be found"}
	orig_list = driver.find_element_by_id('stations_from')
	waitForLoad(driver, 5, 'class', '_1ef1s25')
	orig_opts = orig_list.find_elements_by_class_name('_1ef1s25')
	orig_opts = [unidecode(opt.text) for opt in orig_opts]
	orig_found = False
	for opt in orig_opts:
		if opt == origin[0] or opt == origin[1] or opt == origin[2]: 
			orig_found = True
			break
		else: orig_inp.send_keys(Keys.ARROW_DOWN)
	orig_inp.send_keys(Keys.ENTER)

	if destination[0] == destination[2]:
		dest_inp.send_keys(destination[0])
	else:
		dest_inp.send_keys(destination[1])
	if cancelLoad(driver, 5, 'id', 'stations_to'):
		return {origin[2]:"One city in pair could not be found", destination[2]:"One city in pair could not be found"}
	dest_list = driver.find_element_by_id('stations_to')
	waitForLoad(driver, 5, 'class', '_1ef1s25')
	dest_opts = dest_list.find_elements_by_class_name('_1ef1s25')
	dest_opts = [opt.text for opt in dest_opts] 
	dest_found = False
	for opt in dest_opts:
		if opt == destination[0] or opt == destination[1] or opt == destination[2]: 
			dest_found = True
			break
		else: dest_inp.send_keys(Keys.ARROW_DOWN)
	dest_inp.send_keys(Keys.ENTER)

	#Click search
	time.sleep(3)
	waitForLoad(driver, 3, 'class', '_1tuqvrz4')
	search = driver.find_element_by_class_name('_1tuqvrz4')
	search.click()

	#Get url
	url = driver.current_url

	#Close driver
	driver.close()
	driver.quit()

	#Parse url for ids
	parsed = url.split('origin=')[1]
	parsed = parsed.split('&destination=')
	orig_id = parsed[0]
	dest_id = parsed[1].split('&')[0]

	if not orig_found: orig_id = 'ID not found'
	if not dest_found: dest_id = 'ID not found'

	id_dict = {}
	id_dict[origin[2]] = orig_id
	id_dict[destination[2]] = dest_id

	return id_dict

def scrapeIDsHelper(input_tuple):
	origin, destination = input_tuple
	return scrapeIDs(origin, destination)

#Get local exonyms for every city in the db
def getLocalExonyms():
	#Get city name and country	
	conn = create_connection('../database/wanderweg.db')
	cur = conn.cursor()
	city_sql = 'SELECT name, country FROM cities'
	cur.execute(city_sql)
	city_data = cur.fetchall()
	city_country = {entry[0]:entry[1] for entry in city_data}

	exo_sql = 'SELECT * FROM exonyms'
	cur.execute(exo_sql)
	col_names = [country[0] for country in cur.description[1:]]
	country_index = {country:index+1 for index, country in enumerate(col_names)}
	exonyms = cur.fetchall()
	conn.close()

	#Map cities to their local exonym
	exonym_dict = {}
	for row in exonyms:
		english_index = country_index['england']
		if row[english_index] in city_country.keys():
			cur_city = row[english_index]
			#Get the country for the current city
			country = city_country[cur_city]
			#Get the local city name for the current city
			if country.lower() in country_index:
				local_name = row[country_index[country.lower()]]
			else: 
				local_name = cur_city
			exonym_dict[cur_city] = local_name

	return exonym_dict	

#Build a list of city pairs
def buildCityPairs(safe_city=False, offset=0):
	#Get dict mapping cities to local exonyms
	local_exonyms = getLocalExonyms()
	city_names = []

	for english_name, local_name in local_exonyms.items():
		if filterCities(english_name):
			print(english_name, local_name)
			name_opts = (local_name, local_name + ' (' + english_name + ')', english_name)
			city_names.append(name_opts)

	city_names = city_names[offset:]

	#Format into pairs
	# random.shuffle(city_names)
	city_pairs = []
	#Use rome as the destination so we can ensure that if the origin is valid it will work
	if safe_city:
		safe_entry = ('Roma', 'Roma (Rome)', 'Rome')
		for city in city_names:
			city_pairs.append((city, safe_entry))
	#Use two unknown cities to get move twice as fast
	else:
		for i in range(0, len(city_names), 2):
			if i + 1 < len(city_names):
				city_pairs.append((city_names[i], city_names[i+1]))
			else: 
				city_pairs.append((city_names[i], city_names[0]))
	
	return city_pairs

#Use exonym dict to get all trainline ids for cities in our db
def scrapeAllIDs(city_pairs, num_threads=8):
	pool = ThreadPool(num_threads)
	results = pool.map(scrapeIDsHelper, city_pairs)
	pool.close()
	pool.join()
	
	trainline_ids = {}
	for result in results:
		trainline_ids.update(result)

	print(trainline_ids)
	return trainline_ids

#Add ids to database
def addIDsToDB(trainline_ids):
	db_vals = []
	for key, val in trainline_ids.items():
		if val == 'One city in pair could not be found': continue
		else: db_vals.append((val, key))

	conn = create_connection('../database/wanderweg.db')
	cur = conn.cursor()
	sql = 'UPDATE cities SET trainline_id = ? WHERE name = ?'
	cur.executemany(sql, db_vals)
	conn.commit()
	conn.close()
	
def partitionScraping(step=8, offset=0, safe_city=False):
	city_pairs = buildCityPairs(safe_city, offset)
	for i in range(0, len(city_pairs), step):
		cur_pairs = city_pairs[i:i+step]
		print(cur_pairs)
		ids = scrapeAllIDs(cur_pairs, step)
		addIDsToDB(ids)
		print('Done Adding')

#Helper to check filter cities
def filterCities(city_name):
	# return True

	# filter_names = {'La spezia','Mazara del vallo', 'Milan','Reggio Emilia'}
	# filter_names = {'Bol', 'Brac', 'Brela','Hvar','Korcula','Novalja'}
	filter_names = {'Salerno'}

	for name in filter_names:
		if city_name.lower() in name.lower(): 
			return True
			# return False
	# return True
	return False

#Save DB to csv in case DB is ever deleted
def saveDBToText():
	conn = create_connection('../database/wanderweg.db')
	cur = conn.cursor()
	sql = 'SELECT id, name, trainline_id FROM cities'
	cur.execute(sql)
	data = cur.fetchall()
	string = json.dumps(data)
	f = open('../database/trainline_ids.txt', 'w+')
	f.write(string)
	f.close()

#Loads from a text file
def loadDBFromText():
	with open('../database/trainline_ids.txt', 'r') as f:
		content = f.read()
		data = json.loads(content)
		tuple_data = []
		for entry in data:
			city_id, city_name, trainline_id = entry
			if len(trainline_id) > 20:
				tuple_data.append((trainline_id, city_id, city_name))

		conn = create_connection('../database/wanderweg.db')
		cur = conn.cursor()
		sql = 'UPDATE cities SET trainline_id = ? WHERE id = ? AND name = ?'
		cur.executemany(sql, tuple_data)
		conn.commit()
		conn.close()

base_url = 'https://www.thetrainline.com/'

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('log-level=3')

batch_size = 1
partitionScraping(batch_size, 0, True)

# saveDBToText()
# loadDBFromText()
