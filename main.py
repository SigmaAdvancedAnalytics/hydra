import pprint as pp
import sys
import os
from os import getenv, path
import pickle
import pymssql
import MSSQL_connector as mssql
import results_generator as results


"""
    Hydra is a rapid extraction tool for use in novel data infrastructure environments.
    Its purpose is to provide a wide selection of simple data source handlers which can be manipulated and combined to create
    multi-headed one-shot data extractions for processing in a more powerful cloud environment.
    Given only environment credentials, Hydra will assist with:
        + Enumerating all data elements for target servers
        + Providing summary statistics for later reconciliation
        + Investigating specific elements 
        + Marking elements for extraction
        + Efficient bulk transfer to a cloud or local storage solution
        + Post-transfer reconciliation

    Hydra's purpose is NOT to be a set-and-forget data pipeline as this is better suited to existing pipeline tools such as Spotify's Luigi.
    Instead Hydra should be used to build a solid POC from which a better optimised and tailored pipeline can be built. It balances between
    full-featured libraries for single data sources (i.e. TableauServerClient, AWS CLI), and simple data extractors which limit access 
    to the underlying datasource (i.e. Pandas' IO Tools). This minimises the upfront investment required to develop an inital analytics 
    solution while also avoiding the need for an expensive re-build as the project matures. Simply fork the Hydra repository and expand its 
    pre-built connectors to suit your tailored pipeline. Hydra's handlers are simple to modify by design and will make use of the most 
    extensible data connector available for any given target data source. 

    There are two modules implemented by Hydra:
        1) Inbound - for initial connection and investigation of data sources
        2) Outbound - for efficient bulk transfer of selected data elements
    These are designed for compatibility with the following technologies:
        + Flat files (currently only CSV)
        + IBM Notes (formerly Lotus Notes)
        + SQL Alchemy - MSSQL & PostgreSQL
        + Tableau Server Repository
        + SAP (when integrated with 'SAPsucker')
        + AWS - S3 & RDS

"""
# Config
#output_db_table = 'dbo.maint_lotus_notes'
#update_db = False # Use carefully



# MSSQL details
#SQL Server credentials
SQL_SERVER = 'CA3BSF2-CASQL01'
SQL_DB = 'AgProCanada_TableauDEV'
SQL_USER = getenv("PYMSSQL_USERNAME") #Set this in Powershell using >>> $env:PYMSSQL_USERNAME = "THEKENNAGROUP\Jbarber"
SQL_PASS = getenv("PYMSSQL_PASSWORD") #Set this in Powershell using >>> $env:PYMSSQL_PASSWORD = "Super_SecretPaword"
SQL_PORT = 1433
SQL_DRIVER = 'mssql+pymssql'


#Connect to DB
print('Connecting to SQL server')
sql_conn,sql_session,sql_engine = results.connect(SQL_SERVER,SQL_DB,SQL_USER,SQL_PASS,port=1433,driver=SQL_DRIVER)
 

# load pickle dict
pickle_file = path.dirname(path.realpath(__file__))+'\pickle.p'
print('Loading Pickle file {} into list of dictionaries'.format(pickle_file))
lotus_docs = pickle.load(open(pickle_file, "rb"))


# create table
tablename = 'Lotus_test_11'
print('Creating table {}'.format(tablename))
lotus_attr_dict = results.create_schema(tablename,lotus_docs)
lotus_table,msg = results.create_table(lotus_attr_dict,sql_engine,drop=True)

pp.pprint(lotus_attr_dict)

# Dynamic insert using Dictionary unpacking
print('Inserting {} rows'.format(len(lotus_docs)))
for doc in lotus_docs:
    new_row_vals = lotus_table(**doc)
    sql_session.add(new_row_vals) # Add to session
    sql_session.commit() # Commit everything in session

print('Export complete!')
"TBD Efficient data load"


"""
# Create Tableau workbooks datatable
    conn.execute_non_query(~~~ 
        IF OBJECT_ID('framework.Tableau_workbooks', 'U') IS NOT NULL
            DROP TABLE framework.Tableau_workbooks
        CREATE TABLE [framework].[Tableau_workbooks](
            WorkbookID VARCHAR(100),
            WorkbookName VARCHAR(100), 
            ContentURL VARCHAR(100), 
            ProjectName VARCHAR(100),
            CreatedDate VARCHAR(100), 
            UpdatedDate VARCHAR(100),
            Connections VARCHAR(100)
            )~~~)  

    # Create Tableau connections datatable
    conn.execute_non_query(~~~ 
        IF OBJECT_ID('framework.Tableau_connections', 'U') IS NOT NULL
            DROP TABLE framework.Tableau_connections
        CREATE TABLE [framework].[Tableau_connections](
            ConnectionID VARCHAR(100),
            DatasourceID VARCHAR(100),### 
            DatasourceName VARCHAR(100), 
            ConnectionType VARCHAR(100),
            Username VARCHAR(100),### 
            Password VARCHAR(100), 
            EmbedPassword VARCHAR(100),
            ServerAddress VARCHAR(100),### 
            ServerPort VARCHAR(100)
            )~~~)  

    # Create Tableau views datatable
    conn.execute_non_query(~~~ 
        IF OBJECT_ID('framework.Tableau_views', 'U') IS NOT NULL
            DROP TABLE framework.Tableau_views
        CREATE TABLE [framework].[Tableau_views](
            WorkbookID VARCHAR(100),
            ViewID VARCHAR(100), 
            ViewName VARCHAR(100),
            OwnerID VARCHAR(100),
            TotalViews VARCHAR(100)
            )~~~)  
              
    return conn

    def create_framework_tables(sql_server, user, password, database):
    # Create Lotus report table
    conn.execute_non_query(~~~ 
        IF OBJECT_ID('framework.Lotus_reports', 'U') IS NOT NULL
            DROP TABLE framework.Lotus_reports
        CREATE TABLE [framework].[Lotus_reports](
            FORM VARCHAR(100), 
            DocCode VARCHAR(100), 
            REPORTTYPE VARCHAR(100), 
            SEASON VARCHAR(100), 
            Published VARCHAR(100), 
            Created VARCHAR(100), 
            ReportAccess VARCHAR(100), 
            ReportAccessNames VARCHAR(100), 
            ACLAuthors VARCHAR(100), 
            PDF VARCHAR(100), 
            Workbook VARCHAR(100), 
            Report VARCHAR(100), 
            Width VARCHAR(100), 
            Height VARCHAR(100), 
            FileName VARCHAR(100), 
            ReportName VARCHAR(100), 
            ReportDescription VARCHAR(100), 
            SearchKeywords VARCHAR(100), 
            ACLReaders VARCHAR(100), 
            UpdatedBy VARCHAR(100), 
            Revisions VARCHAR(100) 
            )~~~)


# Export to JSON file if flag set, otherwise STDOUT
if save_to_file:
    jsonarray = json.dumps(reports)
    pp.pprint(jsonarray) #test
    f = open(output_file, "w")
    f.write(jsonarray)
    f.close()
    print('Database output to {}'.format(output_file))
else:
    pp.pprint(reports)
"""


