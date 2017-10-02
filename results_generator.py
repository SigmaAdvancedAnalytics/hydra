# Test implementation of dynamic table generation using SQL Alchemy ORM capabilities
# Taken from http://sparrigan.github.io/sql/sqla/2016/01/03/dynamic-tables.html
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
#import pyodbc - required by sqlalchemy if connecting to MSSQL db


" TODO Get the fucking PYODBC connector working"
SERVER_NAME = 'CA3BSF2-CASQL01'
DATABASE_NAME = 'AgProCanada_TableauDEV'

#Establish windows authenticated session - Not yet tested
engine = create_engine('mssql://'+SERVER_NAME+'/'+DATABASE_NAME)

#Required for 'declarative' use of the SQLAlchemy ORM
Base = declarative_base()

class MyTableClass(Base):
    __tablename__ = 'myTableName'
    myFirstCol = Column(Integer, primary_key=True)
    mySecondCol = Column(Integer, primary_key=True)


Base.metadata.create_all(engine)


"""
#Use of Type() to dynamically generate columns. More detail here: http://sahandsaba.com/python-classes-metaclasses.html#metaclasses
attr_dict = {'__tablename__': 'Lotus_Test_1OCT',
	     'myFirstCol': Column(Integer, primary_key=True),
	     'mySecondCol': Column(Integer)}
#Create table from dictionary specified columns
MyTableClass = type('MyTableClass', (Base,), attr_dict)
Base.metadata.create_table(engine)

# Dynamic insert using Dictionary unpacking
firstColName = "Ill_decide_later"
secondColName = "Seriously_quit_bugging_me"

new_row_vals = MyTableClass(**{firstColName: 14, secondColName: 33})
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
    conn = _mssql.connect(server=sql_server, user=user, password=password, database=database)
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
