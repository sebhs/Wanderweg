from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from urllib3.exceptions import MaxRetryError
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool
import sys
sys.path.append('../database')
from db_utils import create_connection


base_url = 'https://www.thetrainline.com/book/results?origin=_ORIG_&destination=_DEST_&outwardDate=_DATE_T10%3A00%3A00&outwardDateType=departAfter&journeySearchType=single&passengers%5B%5D=1993-03-12%7C39e086e7-d9a3-4b99-83c8-13398ea86824&selectedOutward=e4%2BA34QkjGc%3D%3AnXL1onjhxgY%3D%3AStandard'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=3')

#Fetch trainline id using the city id we store in our db
def fetchID(sql_id):
    conn = create_connection('./database/wanderweg.db')
    cur = conn.cursor()
    sql = "SELECT trainline_id FROM cities WHERE id = '" + sql_id + "'"
    cur.execute(sql)
    data = cur.fetchone()

    trainline_id = data[0]
    if trainline_id == '0' or trainline_id == 'ID not found':
        trainline_id = None
    return trainline_id

def elementLoads(driver, by, val, secs=3):
    try:
        WebDriverWait(driver, secs).until(EC.presence_of_element_located((by, val)))
        print("Element loaded")
        return True
    except TimeoutException:
        print("Element doesn't load")
        return False

def elementClickable(driver, by, val, secs=3):
    try:
        WebDriverWait(driver, secs).until(EC.element_to_be_clickable((by, val)))
        print("Element clickable")
        return True
    except TimeoutException:
        print("Element not clickable")
        return False

def scrapeRows(soup, trip_type='train'):
    route_options = []
    rows = soup.find_all('div', class_='_dbqts5')
    for row in rows:
        opt = {}
        spans = row.find_all('span')
        for i, span in enumerate(spans):
            if i == 0: opt['departure_time'] = span.text
            if i == 1 : opt['arrival_time'] = span.text
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

def scrapeTrains(origin, destination, date='2019-04-10'):
    #Define trip options
    trip_opts = {}
    trip_opts['meta'] = {'orig_id':origin, 'dest_id':destination, 'date':date}
    trip_opts['trip_info'] = [[], [], []]

    orig_id = fetchID(origin)
    dest_id = fetchID(destination)
    if not orig_id or not dest_id:
        print("ID not found for one or more cities")
        trip_opts['meta']['mssg'] = 'ID not found for one or more cities'
        return trip_opts

    url = base_url.replace('_ORIG_', orig_id).replace('_DEST_', dest_id).replace('_DATE_', date)
    trip_opts['meta']['url'] = url

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

    #Wait for page to load
    if not elementLoads(driver, By.CLASS_NAME, '_1i7lx6zm', 5):
        driver.close()
        driver.quit()
        trip_opts['meta']['mssg'] = "Couldn't load page"
        return trip_opts

    #Scrape train info
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    route_options = scrapeRows(soup)

    #Scrape bus info
    if elementClickable(driver, By.CLASS_NAME, '_17dn4adNaN'):
        bus_button = driver.find_element_by_class_name('_17dn4adNaN')
        try:
            bus_button.click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html5lib')
            route_options += scrapeRows(soup, 'bus')
        except WebDriverException:
            print('Error scraping bus info')

    driver.close()
    driver.quit()

    cheapest, fastest, bus = formatOptions(route_options)
    trip_opts['meta']['mssg'] = "Trips found"
    trip_opts['trip_info'] = [bus, cheapest, fastest]

    return trip_opts

def scrapeHelper(input_tuple):
    origin, destination, date = input_tuple
    test = scrapeTrains(origin, destination, date)
    return test

#Sort options by a few metrics
def formatOptions(trip_options, n=3):
    train_options = [opt for opt in trip_options if opt['type'] == 'train']
    cost_sort = sorted(train_options, key=lambda x: (-float(x['price'])), reverse=True)
    time_sort = sorted(train_options, key=lambda x: x['duration'])
    bus_options = [opt for opt in trip_options if opt['type'] == 'bus']
    bus_options = sorted(bus_options, key=lambda x: (-float(x['price'])), reverse=True)

    return (cost_sort[:n], time_sort[:n], bus_options[:n])

#Take a list of city_ids and dates and use a threadpool to scrape info for each trip
def scrapeList(trip_list, num_threads=8):
    pool = ThreadPool(num_threads)
    results = pool.map(scrapeHelper, trip_list)
    pool.close()
    pool.join()
    print(results)
    return results
