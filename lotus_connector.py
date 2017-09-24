#from lnlib import (get_session, list_views, list_documents,
#    describe_document, search, fetch_documents_since)
import pywintypes
from win32com.client import Dispatch, makepy
makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
makepy.GenerateFromTypeLibSpec('IBM Notes Automation Classes')

SERVER_NAME = 'Toronto16/BASFPro'
DB_NAME = r"BASF\agprocan\agcreports.nsf"
DB_VIEW = 'Tableau Report Config'


def get_session(ln_key, workdir=None):
    "helper function for creating a new NotesSession"
    if workdir:
        os.chdir(workdir)
    session = Dispatch('Lotus.NotesSession')
    session.Initialize(ln_key)
    return session

def list_views(db):
    "list views in database"
    for view in db.Views:
        yield view


def list_documents(view):
    "a helper function for listing documents easily in for loops"
    doc = view.GetFirstDocument()
    while doc:
        yield doc
        doc = view.GetNextDocument(doc)

def describe_view(view):
    "describe view and first document"
    doc = view.GetFirstDocument()
    print('View:', view.Name)
    describe_document(doc)


def describe_document(doc):
    "describe document"
    items = []
    for key in doc.Items:
        item = doc.GetFirstItem(key.Name)
        val = doc.GetItemValue(item.Name)
        r = (item.Name, val)
        items.append(r)
    items.sort()
    for i in items:
        print(i)

def _dt(obj):
    "convert pywintypes.Time to datetime"
    if not type(obj) == type(pywintypes.Time(1)):
        return obj
    else:
        return windt2datetime(obj)
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


session = get_session(ln_key="OldUser34#$") #,workdir=r"C:\Users\jbarber\AppData\Local\IBM\Notes"
db = session.GetDatabase(SERVER_NAME, DB_NAME)

for view in list_views(db):
	print(view.Name)
	for doc in list_documents(view):
		describe_document(doc)
	

reports,dupes = lotus_export_read(input_file)
print('There were {0} reports imported; {1} of which were duplicates'.format(len(reports),len(dupes)))




"""
	for item in doc.Items:
		val = doc.GetItemValue(Item.Name)
		print(Item.Name,' : ',val)
		


#Database > View > Doc > Item.Values

import win32com.client
session = win32com.client.Dispatch('Lotus.NotesSession')
session.Initialize(r'pppppppp')
db = session.GetDatabase('',r'dddddddd.nsf')
view = db.GetView(r'vvvvvvvv')
doc = view.GetFirstDocument()
print doc.GetFirstItem('iiiiii').Values
"""