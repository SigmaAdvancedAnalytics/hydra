from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymssql
import pickle
import sys
from os import getenv, path
import pprint as pp

def dict_attributes(source):
    "return dictionaries attributes required to generate table schema"
    fieldnames = dict(set().union(*(dict.keys() for dict in source))) #create a unique set of all dict keys
    print(fieldnames)
    for dict in source:
        max_len=max(dict, key=lambda k: len(dict[k]))
    
    return fieldnames,len(dict[max_len]), max_len


def connect(host,dbname,user,password,port=1433,driver='mssql+pymssql'): #1433 is default MSSQL port
    "Helper function for creating MSSQL db connection"
    #'driver://user:password@hostname:port/database_name'
    engine = create_engine('{}://{}:{}@{}:{}/{}'.format(driver,user,password,host,port,dbname))
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session() # I wonder if we can collapse these using a Lambda
    return conn,session,engine

def create_schema(tablename,source): #TODO figure out how to sort columns - ordered dicts etc. seem to have no effect
    "Create sqlalchemy table from dictionary specified columns"
    #Create a dictionary of the required table attributes - clever but not quite wizardry
    fields = list(set().union(*(dict.keys() for dict in source))) #create a unique set of all dict keys
    fields.sort()
    attr_dict = dict(((field,Column(String(800)) ) for field in fields)) #turn each key into a String(varchar) column
    attr_dict['ID'] = Column(Integer, primary_key=True) # add a PK - SQLAlchemy demands this
    attr_dict['__tablename__'] = tablename #tablename assignment is done inside the dictionary
    return attr_dict

def create_table(attr_dict,engine,drop=False): #TODO order the fields
    "Create table from dictionary attributes"
    #Dark, dark SQLAlchemy metaclass magic - taken from http://sparrigan.github.io/sql/sqla/2016/01/03/dynamic-tables.html
    Base = declarative_base() #Required for 'declarative' use of the SQLAlchemy ORM
    GenericTableClass = type('GenericTableClass', (Base,), attr_dict) #Use of Type() to dynamically generate columns. More detail here: http://sahandsaba.com/python-classes-metaclasses.html#metaclasses
    if drop:
        Base.metadata.drop_all(engine) #Drop all tables in the scope of this metadata
    Base.metadata.create_all(engine) #Create all tables in the scope of this metadata
    return GenericTableClass,'Table {} successfully created'.format(attr_dict['__tablename__'])

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
sql_conn,sql_session,sql_engine = connect(SQL_SERVER,SQL_DB,SQL_USER,SQL_PASS,port=1433,driver=SQL_DRIVER)
 

# load pickle dict
pickle_file = path.dirname(path.realpath(__file__))+'\pickle.p'
print('Loading Pickle file {} into list of dictionaries'.format(pickle_file))
lotus_docs = pickle.load(open(pickle_file, "rb"))


fields = list(set().union(*(dict.keys() for dict in lotus_docs))) #create a unique set of all dict keys
fields.sort()

fields_dict = {}
for field in fields:
    max_val = []
    for doc in lotus_docs:
        if field in doc:
            max_val.append(len(doc[field]))
    fields_dict[field] = max(max_val)
pp.pprint(fields_dict)

attr_dict = dict(((field,Column(String(fields_dict[field])) ) for field in fields_dict)) #turn each key into a String(varchar) column
pp.pprint(attr_dict)





"""
# create table
tablename = 'Lotus_test_11'
print('Creating table {}'.format(tablename))
lotus_attr_dict = create_schema(tablename,lotus_docs)
lotus_table,msg = create_table(lotus_attr_dict,sql_engine,drop=True)

pp.pprint(lotus_attr_dict)

# Dynamic insert using Dictionary unpacking
print('Inserting rows')
for doc in lotus_docs:
    new_row_vals = lotus_table(**doc)
    sql_session.add(new_row_vals) # Add to session
    sql_session.commit() # Commit everything in session

print('Export complete!')

"""


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

"""
    
"""
if update_db:
    create_table()
    for report in reports:
        data = reports[report]
        fields = ['FORM', 'DocCode', 'REPORTTYPE', 'SEASON', 'Published', 'ReportAccess',
        'Workbook', 'Report', 'Width', 'Height', 'FileName',
        'ReportName', 'ReportDescription', 'SearchKeywords', 'UpdatedBy']
        values = data.values()

        print("INSERT INTO table {0} VALUES ({1});" % (','.join(fields), *values))
"""

""" Reference examples of the original SQLAlchemy syntax

#Table creation
	#Required for 'declarative' use of the SQLAlchemy ORM
	Base = declarative_base()

	#Explicitly defined columns example
	class MyTableClass(Base):
		__tablename__ = 'Test_table'
		myFirstCol = Column(Integer, primary_key=True)
		mySecondCol = Column(Integer, primary_key=True)
	Base.metadata.create_table(engine)

# Row insertion
	new_row_vals = MyTableClass(myFirstCol=14, mySecondCol=33)

	session.add(new_row_vals) # Add to session
	session.commit() # Commit everything in session

# Specify columns for insertion
	firstColName = "Ill_decide_later"
	secondColName = "Seriously_quit_bugging_me"

	new_row_vals = MyTableClass(firstColName=14, secondColName=33)






output_file = 'ag_database.json'

# Get a list of report names created after a certain date
spamWriter = csv.writer(open(output_file, 'w',newline=''))
spamWriter.writerow(['Report type', 'Published Status','Created Date', 'Report', 'Description', 'Report Access'])
for report in reports:
    created_date = time.strptime(reports[report]['Created'][:10], "%m/%d/%Y")
    if created_date >= target_date:
        print(reports[report])
        spamWriter.writerow((reports[report]['REPORTTYPE'], reports[report]['Published'], reports[report]['Created'], reports[report]['ReportName'],reports[report]['ReportDescription'],reports[report]['ReportAccess']))



# Begin database connection
if update_db:
    conn = db_test()
    #Test 1
    output = conn.execute_query('SELECT * FROM [dbo].[persons]')
    for row in conn:
        print(row)
    #Test 2
    output[] = conn.execute_query('SELECT [id] FROM [dbo].[persons]')
    for row in conn:
        print(row)
"""


"""

        
try:
    conn.execute_non_query('CREATE TABLE t1(id INT, name VARCHAR(50))')
except _mssql.MssqlDatabaseException as e:
    if e.number == 2714 and e.severity == 16:
        # table already existed, so quieten the error
    else:
        raise # re-raise real error
finally:
    conn.close(




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






        
try:
    conn.execute_non_query('CREATE TABLE t1(id INT, name VARCHAR(50))')
except _mssql.MssqlDatabaseException as e:
    if e.number == 2714 and e.severity == 16:
        # table already existed, so quieten the error
    else:
        raise # re-raise real error
finally:
    conn.close(




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
