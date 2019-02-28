# Overview:
	- This folder holds the database (wanderweg.db) with tables as outlined below
	- Other files are database utilities that initialize the database or static data
	  that is loaded into the db

# Files:
	- countries/<country>Data.txt:
	  Data on all cities supported in <country> such as hostel_url, population, latitude, and longitude

	- db_utils.py:
	  Utility functions for connecting to and querying the database

	- init_db.py:
	  Creates and fills wanderweg.db with data from the files in countries. Should only need to be run once

	- wanderweg.db:
	  Database with static data for easy querying. Tables in wanderweg.db are described below
	
	- weatherbase_cities.csv:
	  List of the urls for all cities supported by weatherbase. Weather averages are scraped from these urls

# Database Info

- If on MacOS, sqlite3 is probably already installed, otherwise you need to download sqlite from https://www.sqlite.org/download.html
- Run "sqlite3" in command line from Wanderweg folder
- Running ".open database/wanderweg.db" in sqlite3 connects to the database
- When adding data to database with python, must call commit() on the connection object
- Unsure if init_db.py needs to be run more than once

# Useful sqlite command line commands
- .open : connects to a database
- .tables : lists all tables in the connected database
- select * from <database>;

# Tables
- cities
	- id: integer
	- name: text
	- country: text
	- hostel_url: text
	- population: integer
	- latitude: real
	- longitude: real

