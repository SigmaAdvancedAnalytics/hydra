import pprint as pp
import sys
import os
from os import getenv
import pickle
import pymssql
import MSSQL_connector as mssql


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


#SQL Server credentials
SQL_SERVER = 'CA3BSF2-CASQL01'
SQL_DB = 'AgProCanada_TableauDEV'
SQL_USER = getenv("PYMSSQL_USERNAME") #Set this in Powershell using >>> $env:PYMSSQL_USERNAME = "THEKENNAGROUP\Jbarber"
SQL_PASS = getenv("PYMSSQL_PASSWORD") #Set this in Powershell using >>> $env:PYMSSQL_PASSWORD = "Super_SecretPaword"


#Tableau connector 

# load pickle dict
pickle_file = os.path.dirname(os.path.realpath(__file__))+'\pickle.p'
lotus_docs = pickle.load(open(pickle_file, "rb"))

#Connect to sql server
"SQL connector export"
conn = mssql.connect(SQL_SERVER,SQL_DB,SQL_USER,SQL_PASS)
mssql.create_lotus_table(conn)

fields = ['FORM', 'DocCode', 'REPORTTYPE', 'SEASON', 'Published', 'ReportAccess',
        'Workbook', 'Report', 'Width', 'Height', 'FileName',
        'ReportName', 'ReportDescription', 'SearchKeywords', 'UpdatedBy']

for doc in lotus_docs:
    keys = []
    values = []
    for k, v in doc.items():
        if k in fields:
            keys.append(k)
            values.append(str(';'.join(v)))
    conn.execute_non_query("""
       IF OBJECT_ID('framework.Lotus_reports', 'U') IS NOT NULL 
       INSERT INTO framework.Lotus_reports ({0})
        VALUES ('{1}')
    """.format(','.join(keys),"','".join(values)))
    

# MSSQL details
#SQL Server credentials
SQL_SERVER = 'CA3BSF2-CASQL01'
SQL_DB = 'AgProCanada_TableauDEV'
SQL_USER = getenv("PYMSSQL_USERNAME") #Set this in Powershell using >>> $env:PYMSSQL_USERNAME = "THEKENNAGROUP\Jbarber"
SQL_PASS = getenv("PYMSSQL_PASSWORD") #Set this in Powershell using >>> $env:PYMSSQL_PASSWORD = "Super_SecretPaword"
SQL_PORT = 1433
SQL_DRIVER = 'mssql+pymssql'

conn,engine = connect(SQL_SERVER,SQL_DB,SQL_USER,SQL_PASS,port=1433,driver=SQL_DRIVER)

# List tables
print("Database tables:\n")
results = list_tables(conn)
pp.pprint(results)  

"Results generator"
"TBD Efficient data load"




