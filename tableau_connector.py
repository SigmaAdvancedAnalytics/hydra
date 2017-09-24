#!/usr/bin/python
import psycopg2
import sys
 
#Define our connection string
conn_string = "host='10.101.191.13' dbname='workgroup' user='readonly' password='KennaG123' port='8060'"

# print the connection string we will use to connect
print("Connecting to database\n	->%s" % (conn_string))

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()
print("Connected!\n")

#KennaG123