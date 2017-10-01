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
