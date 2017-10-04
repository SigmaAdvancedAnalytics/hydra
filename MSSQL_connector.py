from pymssql import _mssql

def connect(sql_server,database,user,password):
    "helper function for creating a new db connection"
    conn = _mssql.connect(server=sql_server, database=database, user=user, password=password)
    return conn


def exec_procedure(session, proc_name, params): #to be completed
    "execute stored procedure"
    sql_params = ",".join(["@{0}={1}".format(name, value) for name, value in params.items()])
    sql_string = """
        DECLARE @return_value int;
        EXEC    @return_value = [dbo].[{proc_name}] {params};
        SELECT 'Return Value' = @return_value;
    	""".format(proc_name=proc_name, params=sql_params)

    return session.execute(sql_string).fetchall()


# Create Lotus report table
def create_lotus_table(conn):
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

	