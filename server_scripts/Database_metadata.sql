/* Database metedata tool*/
/* Notes:
	+ Views should be lowest in the Hierarchy
	+ Currently cannot tell whether procedure creates table or only accesses it
	+ Temp tables will likely be replaced with semi-permanent [framework] schema tables
*/

/* Enumerate all tables on current DB */
IF OBJECT_ID('TEMPDB..#tables') IS NOT NULL DROP TABLE #tables
SELECT  
		 [TABLE_ID]			 = [OBJECT_ID]
		,[TABLE_NAME]		 = [NAME]
		,[TABLE_TYPE]		 = [TYPE_DESC]
		,[TABLE_CREATE_DATE] = [CREATE_DATE]
		,[TABLE_MODIFY_DATE] = [MODIFY_DATE]
	--INTO #tables
FROM sys.tables where name like '%salesdashboard%' or name like '%transa%'
order by modify_date desc

/* Enumerate all views on current DB */
IF OBJECT_ID('TEMPDB..#views') IS NOT NULL DROP TABLE #views
SELECT  
		 [VIEW_ID]			 = [OBJECT_ID]
		,[VIEW_NAME]		 = [NAME]
		,[VIEW_TYPE]		 = [TYPE_DESC]
		,[VIEW_CREATE_DATE] = [CREATE_DATE]
		,[VIEW_MODIFY_DATE] = [MODIFY_DATE]
	INTO #views
FROM sys.views

/* Enumerate all Routines (i.e. procedures and functions) and */
IF OBJECT_ID('TEMPDB..#routines') IS NOT NULL DROP TABLE #routines
SELECT 
			rt1.[ROUTINE_CATALOG]
			,rt1.[ROUTINE_SCHEMA]
			,rt1.[ROUTINE_TYPE]
			,rt1.[ROUTINE_NAME]
			,[ROUTINE_CREATED_DATE] = rt1.[CREATED]
			,[ROUTINE_LAST_ALTERED_DATE] = rt1.[LAST_ALTERED]
			,rt1.[ROUTINE_DEFINITION] 
			,[SUB_ROUTINES] = COUNT(rt2.[ROUTINE_NAME])
			,[SUB_VIEWS] = COUNT(views.[TABLE_NAME])
	INTO #routines
FROM information_schema.routines rt1
LEFT JOIN information_schema.routines rt2 ON rt1.[ROUTINE_NAME] = (CASE PATINDEX('%'+rt1.[ROUTINE_NAME]+'%',rt2.[ROUTINE_DEFINITION]) WHEN 0 THEN NULl ELSE rt1.[ROUTINE_NAME] END)
LEFT JOIN information_schema.views views ON (CASE PATINDEX('%'+views.[TABLE_NAME]+'%',rt1.[ROUTINE_DEFINITION]) WHEN 0 THEN NULl ELSE views.[TABLE_NAME] END) = views.[TABLE_NAME]
GROUP BY rt1.[ROUTINE_CATALOG]
		 ,rt1.[ROUTINE_SCHEMA]
		 ,rt1.[ROUTINE_TYPE]
		 ,rt1.[ROUTINE_NAME]
		 ,rt1.[CREATED]
		 ,rt1.[LAST_ALTERED]
		 ,rt1.[ROUTINE_DEFINITION]

/* Identify views referenced by a routine */
SELECT *
FROM #views
LEFT JOIN #routines
ON [VIEW_NAME] = (CASE PATINDEX('%'+[VIEW_NAME]+'%',[ROUTINE_DEFINITION]) WHEN 0 THEN NULl ELSE [VIEW_NAME] END)

/* Identify routines that reference other routines, and join in their children */
SELECT rt2.*,':',rt1.*
FROM #routines rt1
LEFT JOIN #routines rt2
ON rt1.[ROUTINE_NAME] = (CASE PATINDEX('%'+rt1.[ROUTINE_NAME]+'%',rt2.[ROUTINE_DEFINITION]) WHEN 0 THEN NULl ELSE rt1.[ROUTINE_NAME] END)
WHERE RT2.[ROUTINE_NAME] IS NOT NULL
ORDER BY RT2.[ROUTINE_NAME] DESC

/* Join routines to the tables they directly reference by searching the procedure definition for references to the table*/
IF OBJECT_ID('framework.SQL_dependencies') IS NOT NULL DROP TABLE framework.SQL_dependencies
SELECT 
	  tables.*
	  ,routines.*
	INTO framework.[SQL_dependencies]
FROM #tables tables
LEFT JOIN #routines routines
ON [TABLE_NAME] = (CASE PATINDEX('%'+[TABLE_NAME]+'%',[ROUTINE_DEFINITION]) WHEN 0 THEN NULl ELSE [TABLE_NAME] END)


/* Access procedure usage data TBD */
SELECT * FROM [AgProCanada_TableauDEV].[framework].[ProcedureLog]

/*Add this to procedures to ensure they're captured by the log 
  Set @AdditionalInfo to pass any notes on the procedure*/
--EXEC framework.Log_ProcedureCall_p @ObjectID = @@PROCID, @AdditionalInfo = NULL; --For Reference: 

/*DEPRECATED CODE*/
/* Table creation
IF OBJECT_ID('TEMPDB..#test') IS NOT NULL DROP TABLE #test
CREATE TABLE #test([Field] [varchar](100) NULL) ON [PRIMARY]
INSERT INTO #test  VALUES('#budget') 
Select * from #test

/* Search for table references*/
SELECT Name, object_id, OBJECT_DEFINITION(OBJECT_ID)
FROM sys.procedures
WHERE OBJECT_DEFINITION(OBJECT_ID) LIKE '%'+(SELECT TOP 1 * FROM #test)+'%'

/* View data */
SELECT [OBJECT_ID], [NAME], [TYPE_DESC], [CREATE_DATE], [MODIFY_DATE] FROM sys.views

/*Function Data*/
SELECT [ROUTINE_CATALOG], [ROUTINE_SCHEMA], [ROUTINE_TYPE], [ROUTINE_NAME], [CREATED], [LAST_ALTERED], [ROUTINE_DEFINITION] FROM information_schema.routines 
SELECT Table_name, max(ordinal_position) as Longest FROM INFORMATION_SCHEMA.columns group by TABLE_NAME order by Longest DESC;*/
