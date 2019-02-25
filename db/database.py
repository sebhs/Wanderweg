import sqlite3
from sqlite3 import Error
import db.buildCityList as bcl

'''
This file loads the database with scraped data
'''
 
def create_connection(db_file=".\sqlite.db"):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_cities(conn, city_info):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    row_sql = """   INSERT INTO city_data(id, name, country, hostel_url, population, latitude, longitude)
                    VALUES(?,?,?,?,?,?,?)
                """
    cur = conn.cursor()
    cur.executemany(row_sql, city_info)
    return cur.lastrowid

#Loads data for cities in Italy
def load_italian_data():
    #Scrapes data from online
    # italianCities= bcl.buildCityMap('https://www.hostelworld.com/hostels/Italy')
    # bcl.addPopulationData('Italy', italianCities)
    # bcl.prune(italianCities, 3)
    # bcl.addCoordData(italianCities)

    #Reads from text file
    italianCities = bcl.readFromFile('italyData.txt')
    
    return italianCities

def update_city_data(conn):
   
    #Create table if necessary
    city_table_sql = """ CREATE TABLE IF NOT EXISTS city_data (
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
        create_table(conn, city_table_sql)
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
    #Connect to database
    database = ".\sqlite.db"
    conn = create_connection(database)
    
    #Update the city_data table
    update_city_data(conn)
    

if __name__ == '__main__':
    main()
