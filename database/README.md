# Database Info

- If on MacOS, sqlite3 is probably already installed, otherwise you need to download sqlite from https://www.sqlite.org/download.html
- Run "sqlite3" in command line from Wanderweg folder
- Running ".open database/wanderweg.db" in sqlite3 connects to the database
- When adding data to database with python, must call commit() on the connection object
- Unsure if init_db.py needs to be run more than once

### Useful sqlite command line commands
- .open : connects to a database
- .tables : lists all tables in the connected database
- select * from <database>

### Tables
- cities
	- id: integer
	- name: text
	- country: text
	- hostel_url: text
	- population: integer
	- latitude: real
	- longitude: real

