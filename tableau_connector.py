#!/usr/bin/python
import pandas as pd
import sqlalchemy
import psycopg2
import pprint as pp
 #https://onlinehelp.tableau.com/current/server/en-us/data_dictionary.html


def connect(host,dbname,user,password,port=5432,driver='postgresql+psycopg2'): #5432 is default Postgres port
    "helper function for creating postgres db connection"
    #'postgresql+psycopg2://user:password@hostname/database_name'
    engine = sqlalchemy.create_engine('{}://{}:{}@{}:{}/{}'.format(driver,user,password,host,port,dbname))
    conn = engine.connect()
    return conn,engine

def list_tables(conn):
    "return a tuple of all tables in PostgreSQL database"
    results = conn.execute("""
                SELECT table_schema || '.' || table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                AND table_schema NOT IN ('pg_catalog','information_schema');
                """) 
    results_list = [row[0] for row in results]
    results_list.sort()
    return results_list

def get_table(tablename,engine,schema):
    df = pd.read_sql_table(tablename, engine,schema)
    return df

def exec_query():
    return True
    #the_frame = pd.read_sql_query("SELECT * FROM %s;" % name_of_table, engine)





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
