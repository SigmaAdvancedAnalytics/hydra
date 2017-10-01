def exec_procedure(session, proc_name, params):
    sql_params = ",".join(["@{0}={1}".format(name, value) for name, value in params.items()])
    sql_string = """
        DECLARE @return_value int;
        EXEC    @return_value = [dbo].[{proc_name}] {params};
        SELECT 'Return Value' = @return_value;
    """.format(proc_name=proc_name, params=sql_params)

    return session.execute(sql_string).fetchall()

#SQL Server authentication
sql_server = 'CA3BSF2-CASQL01'
database = 'AgProCanada_TableauDEV'
user = getenv("PYMSSQL_USERNAME") #Set this in Powershell using >>> $env:PYMSSQL_USERNAME = "THEKENNAGROUP\Username"
password = getenv("PYMSSQL_PASSWORD") #Set this in Powershell using >>> $env:PYMSSQL_PASSWORD = "Super_SecretPaword"

"""
		Uses the config.ini file to esablish both the sql_alchemy and psycopg2 connections to the database, then connects to the local csv file
			Note: the dual connections are for maximum efficiency in bulk uploads. Psycopg2 has a significantly faster transfer rate and is used for transferring the files,
			however the sql_alchemy engine connection and pandas to_sql() function are used initially generate the table for insertion as:
			a) psycopg2 copy_from() does not have functionality to create tables, it can only insert rows
			b) dynamically generating table schema in PostgreSQL is extremely complex, while pandas.to_sql() handles it elegantly
		"""
		try:
			with open("config.yml", 'r') as ymlfile:
				config = yaml.load(ymlfile)
			#set the database connection parameters based on the config.ini file
			host = config['PostgreSQL']['host']
			port = config['PostgreSQL']['port']
			dbname = config['PostgreSQL']['dbname']
			user  = config['PostgreSQL']['user']
			password = config['PostgreSQL']['password']
		except:
			return sys.exc_info()

		try:
			#deprecated: self.allFiles = glob.glob(os.path.join(self.data,"*.csv"))
			self.myfile = data_path
			#establish connections to the postgres database and an active cursor for queries
			self.engine = create_engine(r"postgresql://"+user+":"+password+"@"+host+"/"+dbname)
			self.conn = psycopg2.connect(host=host,port=port,dbname=dbname,user=user,password=password)
			self.cursor = self.conn.cursor()
		except:
			return sys.exc_info()