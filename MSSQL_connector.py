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
        	    FORM VARCHAR(500), 
            	DocCode VARCHAR(500), 
	            REPORTTYPE VARCHAR(500), 
	            SEASON VARCHAR(500), 
	            Published VARCHAR(500), 
	            Created VARCHAR(500), 
	            ReportAccess VARCHAR(500), 
	            ReportAccessNames VARCHAR(500), 
	            ACLAuthors VARCHAR(500), 
	            PDF VARCHAR(500), 
	            Workbook VARCHAR(500), 
	            Report VARCHAR(500), 
	            Width VARCHAR(500), 
	            Height VARCHAR(500), 
	            FileName VARCHAR(500), 
	            ReportName VARCHAR(500), 
	            ReportDescription VARCHAR(500), 
	            SearchKeywords VARCHAR(500), 
	            ACLReaders VARCHAR(500), 
	            UpdatedBy VARCHAR(500), 
	            Revisions VARCHAR(500) 
            )""")

	