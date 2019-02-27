import sys
sys.path.append('..')
import sqlite3
from sqlite3 import Error
from pathlib import Path
from dataCollection import buildCityList as bcl
from database import db_utils as db

'''
This file loads the database with scraped data
'''

def add_cities(conn, city_info):
    row_sql = """   INSERT INTO city_features(id, name, country, hostel_url, population, latitude, longitude)
                    VALUES(?,?,?,?,?,?,?)
                """
    cur = conn.cursor()
    cur.executemany(row_sql, city_info)
    return cur.lastrowid

#Loads data for cities in Italy
def load_italian_data():
   
    #Reads from text file
    italyPath = str(Path('.\italyData.txt').resolve())
    italianCities = bcl.readFromFile(italyPath)
    
    return italianCities

def update_city_tables(conn):
   
    #Create table for city features 
    city_features_sql = """ CREATE TABLE IF NOT EXISTS city_features (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        country text NOT NULL,
                                        hostel_url text,
                                        population integer,
                                        latitude real,
                                        longitude real
                                    ); """

    #Create the table and fill it in
    if conn is not None:
        #Create tables
        db.create_table(conn, city_features_sql)

        #Load data 
        # TODO: Expand to more countries 
        italianCities = load_italian_data()

        city_tups = []
        city_id = 0
        for city, info in italianCities.items():
            city_tups.append((city_id, city, info[0], info[1], info[2], info[3], info[4]))
            city_id += 1

        add_cities(conn, city_tups)

        conn.commit()
        conn.close()

    else:
        print("Error! cannot create the database connection.")

def main():
    #Set path
    database_str = str(Path.cwd() / 'sqlite.db')

    #Connect to database
    conn = db.create_connection(database_str)
    
    #Update the city_data table
    update_city_tables(conn)
    
main()