input_file = 'ag_database.text'

# Init variables
unique = set()
dupe = []
reports = {}
curdict = {}
reportname = ''
workbooks_list = []
connections_list = []
views_list = []

# Read the database file into a dictionary of dictionaries, each nested dictionary representing an individual report

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


reports,dupes = lotus_export_read(input_file)
print('There were {0} reports imported; {1} of which were duplicates'.format(len(reports),len(dupes)))