import pprint as pp
import sys
from os import getenv
from pymssql import _mssql
import tableauserverclient as TSC

input_file = 'ag_database.text'
output_db_table = 'dbo.maint_lotus_notes'
update_db = False # Use carefully

#Tableau Server authentication TODO: convert to .ENV file
tableau_auth = TSC.TableauAuth('jmayer', 'jmayer')
tab_server = TSC.Server('https://reports2.agconnect.org/')
#Additional tab server information will be available here: https://onlinehelp.tableau.com/current/server/en-us/data_dictionary.html
#SQL Server authentication
sql_server = 'CA3BSF2-CASQL01'
database = 'AgProCanada_TableauDEV'
user = getenv("PYMSSQL_USERNAME") #Set this in Powershell using >>> $env:PYMSSQL_USERNAME = "THEKENNAGROUP\Username"
password = getenv("PYMSSQL_PASSWORD") #Set this in Powershell using >>> $env:PYMSSQL_PASSWORD = "Super_SecretPaword"


#Init variables
unique = set()
dupe = []
reports = {}
curdict = {}
reportname = ''
workbooks_list = []
connections_list = []
views_list = []

#read the database file into a dictionary of dictionaries, each nested dictionary representing an individual report
def lotus_export_read(input_file):
    try:    
        #init variables
        unique = set()
        dupe = []
        reports = {}
        curdict = {}
        reportname = ''
        #Read the lotus reports into a dictionary of dictionaries
        f = open(input_file, 'r', encoding='utf-8')
        for line in f:
            if ':' in line:     #':' denotes a field and should be added to the current dictionary
                items = line.strip('$').split(':', 1)
                curdict[items[0].strip()] = items[1].strip()
            elif line == '~\n': #'~' denotes end of current report
                reportname = curdict['DocCode']
                if reportname not in unique:  #'DocCode' represents unique reports - we use these as keys
                    unique.add(reportname)
                    reports[reportname] = curdict
                    curdict = {}
                else:
                    dupe.append(reportname)                             
        f.close()
        return reports,dupe
    except:
        return sys.exc_info()

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

def create_framework_tables(sql_server, user, password, database):
    conn = _mssql.connect(server=sql_server, user=user, password=password, database=database)
    # Create Lotus report table
    conn.execute_non_query(""" 
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
            )""")

    # Create Tableau workbooks datatable
    conn.execute_non_query(""" 
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
            )""")  

    # Create Tableau connections datatable
    conn.execute_non_query(""" 
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
            )""")  

    # Create Tableau views datatable
    conn.execute_non_query(""" 
        IF OBJECT_ID('framework.Tableau_views', 'U') IS NOT NULL
            DROP TABLE framework.Tableau_views
        CREATE TABLE [framework].[Tableau_views](
            WorkbookID VARCHAR(100),
            ViewID VARCHAR(100), 
            ViewName VARCHAR(100),
            OwnerID VARCHAR(100),
            TotalViews VARCHAR(100)
            )""")  
              
    return conn

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
reports,dupes = lotus_export_read(input_file)
print('There were {0} reports imported; {1} of which were duplicates'.format(len(reports),len(dupes)))


workbooks, connections, views = tableau_server_import(tableau_auth, tab_server)
#for view in views:
 #   print(view)
#print(connections)
#print(views)

#print('There were {0} workbooks, {1} views, and {2} connections imported'.format(len(workbooks),0,connections))
#for wb in workbooks:
    #print(wb.connections)

#conn = create_framework_tables(sql_server, user, password, database)
#print(conn)


"""

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
"""

