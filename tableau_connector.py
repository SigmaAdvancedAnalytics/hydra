#!/usr/bin/python
import psycopg2
import sys
import pprint as pp
import pandas as pd
 #https://onlinehelp.tableau.com/current/server/en-us/data_dictionary.html

def connect(host,dbname,user,password,port=5432): #5432 is default Postgres port
    "helper function for creating postgres db connection"
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    return cursor,conn

def list_tables(cursor):
    "return a tuple of all tables in database"
    cursor.execute("""
                SELECT table_schema || '.' || table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                AND table_schema NOT IN ('pg_catalog', 'information_schema');
                """)
    results = cursor.fetchall()
    results.sort()
    results_list = list(sum(results, ())) #magically turns a list of tuples into a flat list
    return results_list

# Test main
# Tableau repository details
HOST = '10.101.191.13'
DBNAME = 'workgroup'
USER = 'readonly'
PASSWORD = 'KennaG123'
PORT = 8060

# Establish connection and return connection & cursor
print("Connecting to database...")
cursor,conn = connect(HOST,DBNAME,USER,PASSWORD,PORT)
print("Connected!\n")
  
# 
results = list_tables(cursor)
print(results)


#conn_string = "host='10.101.191.13' dbname='workgroup' user='readonly' password='KennaG123' port='8060'"


"""
def tableau_server_import(tableau_auth, tab_server):
    try:
        #Connect to Tableau server
        with tab_server.auth.sign_in(tableau_auth):
            for wb in TSC.Pager(tab_server.workbooks):
                tab_server.workbooks.populate_connections(wb)
                tab_server.workbooks.populate_views(wb)
                workbooks_list.append([wb.id,wb.name,wb.content_url,wb.project_name,wb.created_at.date(),wb.updated_at.date(),wb.connections])
                for con in wb.connections:
                    connections_list.append([con.id,con.datasource_id,con.datasource_name,con.connection_type,con.username,con.password,con.embed_password,con.server_address,con.server_port])
                for view in wb.views:
                    views_list.append([view.workbook_id,view.id,view.name,view.owner_id,view.total_views])
        return workbooks_list, connections_list, views_list
    except:
        return sys.exc_info()        

workbooks, connections, views = tableau_server_import(tableau_auth, tab_server) """


#KennaG123
#SQL alchemy connection example
"""
import sqlalchemy

SERVER_NAME = ''
DATABASE_NAME = ''

#Establish windows authenticated session - Not yet tested
engine = sqlalchemy.create_engine('mssql://'+SERVER_NAME+'/'+DATABASE_NAME+'?trusted_connection=yes')
"""

# DEPRECATED TSC API CONNECTOR - TO BE USED FOR FILE UPLOADS AT LATER DATE
"""

import tableauserverclient as TSC

#Tableau Server authentication TODO: convert to .ENV file
tableau_auth = TSC.TableauAuth('jmayer', 'jmayer')
tab_server = TSC.Server('https://reports2.agconnect.org/')
#Additional tab server information will be available here: https://onlinehelp.tableau.com/current/server/en-us/data_dictionary.html

#Tableau Server authentication TODO: convert to .ENV file
tableau_auth = TSC.TableauAuth('jmayer', 'jmayer')
tab_server = TSC.Server('https://reports2.agconnect.org/')

def tableau_server_import(tableau_auth, tab_server):
    try:
        #Connect to Tableau server
        with tab_server.auth.sign_in(tableau_auth):
            workbooks = TSC.Pager(tab_server.workbooks)
            for wb in workbooks:
                workbooks_list = workbooks_list.add([wb.project_name,wb.name,wb.content_url,wb.created_at.date(),wb.updated_at.date()])
                print(workbooks_list)
        return workbooks_list
    except:
        return sys.exc_info()        


workbooks = tableau_server_import(tableau_auth, tab_server)
#for workbook in workbooks:
 #   print(', '.join(workbook))

"""
