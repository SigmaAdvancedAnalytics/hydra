import pprint as pp
import sys
from os import getenv
from pymssql import _mssql

# Config
input_file = 'ag_database.text'
output_db_table = 'dbo.maint_lotus_notes'
update_db = False # Use carefully
"""
    Hydra is a rapid extraction tool for use in novel target environments.
    Its purpose is to provide a wide selection of simple data source handlers which can be manipulated and combined to create
    multi-headed one-shot data extractions for processing in a more powerful cloud environment.
    Given only environment credentials, Hydra will assist with:
        + Enumerating all data elements for target servers
        + Providing summary statistics for later reconciliation
        + Investigating specific elements 
        + Marking elements for extraction
        + Efficient bulk transfer to a cloud or local storage solution
        + Post-transfer reconciliation

    Hydra's purpose is NOT to be a long-term data pipeline. This is better suited to existing pipeline tools such as Spotify's Luigi.
    Instead, Hydra should be used to build a solid POC from which a better optimised and tailored pipeline can be built. It balances between
    full-featured libraries for single data sources (i.e. TableauServerClient, AWS CLI), and simple data extractors which limit access 
    to the underlying datasource (i.e. Pandas' IO Tools).
    
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
"TBD Scanner"
"Lotus connector import"
"Tableau connector import"
"SQL connector import"
"Join logic"
"Results generator"
"TBD Efficient data load"


