import pprint as pp
import json
import time
import csv
from os import getenv
from pymssql import _mssql


input_file = 'ag_database.text'
output_file = 'report_info.csv'
output_db_table = 'dbo.maint_lotus_notes'
update_db = True # Use carefully

server = 'CA3BSF2-CASQL01'
database = 'AgProCanada_TableauDEV'
user = getenv("PYMSSQL_USERNAME") #Set this in Powershell using >>> env:PYMSSQL_USERNAME = "THEKENNAGROUP\Username"
password = getenv("PYMSSQL_PASSWORD") #Set this in Powershell using >>> env:PYMSSQL_PASSWORD = "Super_SecretPaword"

target_date = time.strptime("08/01/2016","%m/%d/%Y")
report_info = []

unique = set()
dupe = []
reports = {}
curdict = {}
reportname = ''
#test save 

#read the database file into a dictionary of dictionaries, each nested dictionary representing an individual report
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

# Error reporting for duplicate keys
if len(dupe) is not 0:
    print('The following reports are duplicated and therefore were overwritten: ')
    print(*dupe,sep='\n')
    exit()
print('There were %d reports imported' %len(reports))

# Get a list of report names created after a certain date
spamWriter = csv.writer(open(output_file, 'w',newline=''))
spamWriter.writerow(['Report type', 'Published Status','Created Date', 'Report', 'Description', 'Report Access'])
for report in reports:
    created_date = time.strptime(reports[report]['Created'][:10], "%m/%d/%Y")
    if created_date >= target_date:
        print(reports[report])
        spamWriter.writerow((reports[report]['REPORTTYPE'], reports[report]['Published'], reports[report]['Created'], reports[report]['ReportName'],reports[report]['ReportDescription'],reports[report]['ReportAccess']))






"""
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

