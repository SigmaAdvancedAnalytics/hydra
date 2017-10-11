from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymssql

def dict_attributes(dict_list):
    "return dictionaries attributes required to generate table schema"
    fields_dict = {}
    fields = list(set().union(*(dict.keys() for dict in dict_list))) #create a unique set of all dict keys
    fields.sort()
    for field in fields:
        max_val = []
        for dict in dict_list:
            if field in dict:
                max_val.append(len(dict[field]))
        fields_dict[field] = max(max(max_val),1) # give field length a minimum of 1 or it defaults to MAX when assigned as a column
    return fields_dict


def connect(host,dbname,user,password,port=1433,driver='mssql+pymssql'): #1433 is default MSSQL port
    "Helper function for creating MSSQL db connection"
    #'driver://user:password@hostname:port/database_name'
    engine = create_engine('{}://{}:{}@{}:{}/{}'.format(driver,user,password,host,port,dbname))
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session() # I wonder if we can collapse these using a Lambda
    return conn,session,engine

def create_schema(tablename,dict_list): #TODO figure out how to sort columns - ordered dicts etc. seem to have no effect
    "Create sqlalchemy table from dictionary specified columns"
    fields_dict = dict_attributes(dict_list) #Create a dictionary of the required table attributes - clever but not quite wizardry
    attr_dict = dict(((field,Column(String(fields_dict[field])) ) for field in fields_dict)) #turn each key into a String(varchar) column using the max lengths from fields_dict
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
