
# imports
import json
import sqlite3
from sqlite3 import Error
from db_utils import create_connection

'''
This file initializes the exonyms table in the Wanderweg database
'''

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


def create_exonyms_table(database):

    # create a database connection                               
    conn = create_connection(database)

    #Create table for city features 
    sql_create_exonyms_table = """ CREATE TABLE IF NOT EXISTS exonyms (
                                        id integer PRIMARY KEY,
                                        england text NOT NULL,
                                        germany text,
                                        france text,
                                        italy text,
                                        spain text,
                                        portugal text,
                                        brazil text,
                                        sweden text,
                                        poland text,
                                        finland text,
                                        denmark text,
                                        netherlands text,
                                        norwegian text,
                                        czech_republic text,
                                        russia text,
                                        turkey text,
                                        japan text,
                                        korea text,
                                        china text
                                    ); """

    if conn is not None:
        # create exonyms table
        create_table(conn, sql_create_exonyms_table)
    else:
        print("Error! cannot create the database connection.")

    return conn



def create_exo(conn, exo):
    sql = "insert into exonyms values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, exo)
    return cur.lastrowid


def readFromFile(filename):
    ret = {}
    with open(filename) as f:
        data = json.load(f)
        for key in sorted(list(data.keys())):
            ret[key] = data[key]
    return ret


# When we scale, will have to write code to access every text file in cities
def load_exonyms_data(conn):
    # for file in 'countries':
    exonyms = readFromFile('exonyms/italyExos.txt')
    count = 1
    for english, info in exonyms.items():
        if info:
            create_exo(conn, (count, english, info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9],
                info[10], info[11], info[12], info[13], info[14], info[15], info[16], info[17]))
        count += 1


def main():
    database = 'wanderweg.db'
    conn = create_exonyms_table(database)
    load_exonyms_data(conn)
    conn.commit()
    conn.close()


if __name__ == '__main__':  
    main()