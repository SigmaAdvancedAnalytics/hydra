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
