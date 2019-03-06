from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

base_url = 'https://www.thetrainline.com/'

options = webdriver.ChromeOptions()
options.add_argument('headless')

#Helper function that makes sure an element has loaded 
def waitForLoad(driver, secs, by, val):
	if by == "class": by = By.CLASS_NAME
	elif by == "id": by = By.ID

	try:
		WebDriverWait(driver, secs).until(EC.presence_of_element_located((by, val))) 
	except TimeoutException:
		print("Page loaded too slow")
		driver.close()
		driver.quit()

def scrapeIDs(origin, destination):
	driver = webdriver.Chrome(chrome_options=options)
	driver.get(base_url)

	#Navigate to page to input origin and destination
	inputs = driver.find_elements_by_class_name('_b2dtf3NaN')
	orig_inp = inputs[0]
	dest_inp = inputs[1]

	#Select the desired location from the dropdown for origin and destination
	orig_inp.send_keys(origin)
	waitForLoad(driver, 3, 'id', 'stations_from')
	orig_list = driver.find_element_by_id('stations_from')
	waitForLoad(driver, 3, 'class', '_1ef1s25')
	orig_opts = orig_list.find_elements_by_class_name('_1ef1s25')
	orig_opts = [opt.text for opt in orig_opts]
	orig_found = False
	for opt in orig_opts:
		if opt == origin: 
			orig_found = True
			break
		else: orig_inp.send_keys(Keys.ARROW_DOWN)
	orig_inp.send_keys(Keys.ENTER)

	dest_inp.send_keys(destination)
	waitForLoad(driver, 3, 'id', 'stations_to')
	dest_list = driver.find_element_by_id('stations_to')
	waitForLoad(driver, 3, 'class', '_1ef1s25')
	dest_opts = dest_list.find_elements_by_class_name('_1ef1s25')
	dest_opts = [opt.text for opt in dest_opts] 
	dest_found = False
	for opt in dest_opts:
		if opt == destination: 
			dest_found = True
			break
		else: dest_inp.send_keys(Keys.ARROW_DOWN)
	dest_inp.send_keys(Keys.ENTER)

	#Click search
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

	if not orig_found: orig_id = 'Origin not found'
	if not dest_found: dest_id = 'Destination not found'

	return (orig_id, dest_id)

#Function to get ids for every city 
def getAllIDs():
	# 1. Get list of all cities and exonames from database
	# 2. Format into tuples of ('local_name (english_name),'local_name (english_name)')
	# 3. Call scrapeIDs on each tuple
	# 4. Add IDs to cities table in wanderweg.db
	pass

city_ids = scrapeIDs('Roma (Rome)', 'Firenze (Florence)')
print(city_ids)
