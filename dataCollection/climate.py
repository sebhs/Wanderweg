import sys
sys.path.append('..')
import requests
import json

##### Working API but only allows querying one day at a time

def scrapeCity(latitude, longitude, date):
    key = '3309b336efe67ed0ed5269bc35af1795'
    base_url = 'https://api.darksky.net/forecast/{key}/'.format(key=key)

    base_url += str(latitude) + ',' + str(longitude) + ',' + str(date)
    # base_url += '?exclude=currently,minutely,hourly,alerts,flags'
    # print(base_url)
    params = {'exclude':'currently,minutely,hourly,alerts,flags'}
    response = requests.get(base_url, params=params)
    for item in response.json().items():
        print(item)

# scrapeCity(42.3601,-71.0589,255657600)

# import re
# import csv
# import requests
# from bs4 import BeautifulSoup
# import json
# import numpy as np
# # from base64 import b64encode
# from database import db_utils as db

# '''
# Script for gathering climate info on cities. Needs a country and a city 
# and then it can find temp mins and maxes, rain, and sun info
# '''

# db_path = '../database/sqlite.db'

########## Uses the list of urls weatherbase covers to build DB ###############################

# def scrapeUrls():

#     conn = db.create_connection(db_path)
#     if conn is not None:
#         #Add weather to cities without it
#         join_sql = """  SELECT city_features.id, city_features.name, city_features.country, 
#                             city_features.latitude, city_features.longitude, city_weather.url 
#                         FROM city_features
#                         INNER JOIN city_weather
#                         ON city_features.name = city_weather.city 
#                         AND city_features.country = city_weather.country
#                     """
#         cur = conn.cursor()
#         cur.execute(join_sql)
#         city_weather = np.array(cur.fetchall())

#         #Get cities
#         all_cities_sql = "SELECT id, name, country, latitude, longitude FROM city_features"
#         cur.execute(all_cities_sql)
#         all_cities = np.array(cur.fetchall())

#         all_weather = []
#         for city in all_cities:
#             loc = np.where(city_weather[:,0] == city[0])
#             if len(loc[0]) > 0:
#                 print(loc[0])


#     else:
#         print("Error! Cannot create the database connection")
#     # url_list = []
#     # with open('../database/weatherbase_cities.csv', 'rt', encoding="utf8") as f:
#     #     reader = csv.reader(f, delimiter='\t')
#     #     for row in reader:
#     #         url, city, country = row[0].split(',')

#     #         url_list.append((url, city , country))


#     headers = {
#         # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
#         # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#         # "accept-charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
#         # "accept-encoding": "gzip,deflate,sdch",
#         # "accept-language": "en-US,en;q=0.8",
#     }

#     data = []
#     for entry in url_list[1:2]:
#         url, city, country = entry
#         try:
#             #Get response
#             response = requests.get(url, headers)
#             soup = BeautifulSoup(response.content, 'html5lib')
            
#             #Parse climate information
#             #TODO: Do we care about sunny hours or wind speed?
#             monthly_temps = []
#             monthly_rain = []
#             monthly_rain_days = []
#             for i in range(1,13):
#                 monthly_temps.append(soup.select('.data')[i].getText())
#                 cur_rain = soup.select('.data')[i+13].getText().replace('---', '0')
#                 monthly_rain.append(cur_rain)
#                 rain_days = soup.select('.data')[i+26].getText().replace('---', '0')
#                 monthly_rain_days.append(rain_days)
#             #Add to data
#             loc = soup.select('h1')[0].getText()
#             loc = loc.split(',')
#             city = loc[0]
#             country = loc[1]
#             city = {'city':city, 'country': country, 'ave_temps':monthly_temps, 'ave_rain':monthly_rain,
#                     'rain_days':monthly_rain_days}
#             data.append(city)
#         except Exception as e:
#             print(e, "with ", url)
#             pass

#     with open ('results.csv','w') as file:
#         writer=csv.writer(file, delimiter=',')
#         for row in data:
#             print(row)
#             # writer.writerow(row)

# #Takes the list of all cities, enters them into data table
# def buildWeatherTable():

#     #Format file to fill database
#     url_list = []
#     with open('../database/weatherbase_cities.csv', 'rt', encoding='utf8') as f:
#         reader = csv.reader(f, delimiter='\t')
#         for row in  reader:
#             url, city, country = row[0].split(',')
#             url_list.append((url, city, country))

#     #Create new DB table
#     create_weather_sql = """ CREATE TABLE IF NOT EXISTS city_weather (
#                                         url text NOT NULL,
#                                         city text NOT NULL,
#                                         country text NOT NULL,
#                                         UNIQUE(url, city)
#                                     ); """

#     #Connect to database
#     conn = db.create_connection(db_path)
    
#     if conn is not None:

#         #Create table
#         cur = conn.cursor()
#         cur.execute(create_weather_sql)

#         #Fill table
#         fill_sql =  """ INSERT INTO city_weather(url, city, country)
#                         VALUES(?,?,?)
#                     """
#         cur = conn.cursor()
#         cur.executemany(fill_sql, url_list)

#         conn.commit()
#         conn.close()
    
#     else:
#         print("Error! Cannot create the database connection")





# scrapeUrls()
# # buildWeatherTable()

###########   Other Stuff    ############


# # api_key = 'dba7e88b915a415f9f071054192702'
# # https://www.worldweatheronline.com/developer/my/



# # # api_key = 'tGAT9bR4GAD67a3DV5FUScbk9VVpUzMf:aN2ivKpclxDPGfVv'
# # encoded_key = b64encode(b'tGAT9bR4GAD67a3DV5FUScbk9VVpUzMf:aN2ivKpclxDPGfVv')

# # def scrapeCity(longitude, latitude):
# #     #Get token
# #     token_url = 'https://api.awhere.com/oauth/token'
# #     header = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': encoded_key}
# #     body = {'grant_type':'client_credentials'}
# #     token_response = requests.post(token_url, headers=header, data=body)
# #     token = token_response.json()['access_token']

# #     # Note: The API is weird so need to manually add each param to url
# #     url = 'https://api.awhere.com/v1/weather?'

# #     header = {'Authorization': 'Bearer %s' %token}
# #     attributes = ['minTemperature', 'maxTemperature', 'precip', 'accPrecip', 'solar', 'maxWind']

# #     url += 'latitude=' + str(latitude) + '&longitude=' + str(longitude)
# #     url += '&startDate=2107-06-01&temperatureUnits=fahrenheit'
# #     response = requests.get(url, headers=header, allow_redirects=False)
# #     json = response.json()
# #     print(json)

# # scrapeCity(30.5, -90.5)


# # class GatherClimate:

# #     def __init__(self):
# #         self.url_base = 'https://www.climatestotravel.com/climate/'
# #         self.url = None
# #         self.country = None
# #         self.city = None
# #         self.soup = None

# #         self.months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# #     #Scrapes the appropriate page for the given city and gathers climate data
# #     def scrapeData(self, country='Italy', city='Florence'):
# #         self.country = country.lower()
# #         self.city = city.lower()
# #         self.url = self.url_base + self.country + '/' + self.city

# #         with urllib.request.urlopen(self.url) as response:
# #             html = response.read().decode('utf-8')
# #             self.soup = BeautifulSoup(html, 'html.parser')

# #         min_temps = self.gatherRow(klass='min-table', filter_term='Fahrenheit')
# #         max_temps = self.gatherRow(klass='max-table', filter_term='Fahrenheit')
# #         precip_inches = self.gatherRow(klass='precipit-table', filter_term='inches')[:-1]
# #         precip_days = self.gatherRow(klass='precipit-table', filter_term='Days')[:-1]
# #         sunny_hours = self.gatherRow(klass='sole-table')

# #         #Create a JSON object to return
# #         temp_data = {'min_temps': min_temps, 'max_temps': max_temps, 'precip_inches': precip_inches,
# #                     'pricip_days': precip_days, 'sunny_hours': sunny_hours}

# #         return json.dumps(temp_data)

# #     #Gathers a single row of climate data
# #     def gatherRow(self, klass, filter_term=None):
# #         entries = []
# #         rows = self.soup.find_all('tr', class_=klass)
# #         for row in rows:
# #             if filter_term == None or filter_term in row.th['title']:
# #                 for entry in row.find_all('td'):
# #                     entries.append(float(entry.text.replace(',','.')))
# #         return entries