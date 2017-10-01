import pywintypes
from win32com.client import Dispatch, makepy

# Update win32com to use the IBM Notes classes
makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
makepy.GenerateFromTypeLibSpec('IBM Notes Automation Classes')


def connect(ln_key, server_name, db_name, workdir=None):
    "helper function for creating a new NotesSession"
    if workdir:
        os.chdir(workdir)
    session = Dispatch('Lotus.NotesSession')
    session.Initialize(ln_key)
    db = session.GetDatabase(server_name, db_name)
    return db


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


# function test
# Lotus credentials
LN_KEY = "OldUser34#$" #Todo: convert these into a .env file
LN_SERVER_NAME = 'Toronto16/BASFPro'
LN_DB_NAME = r"BASF\agprocan\agcreports.nsf"
LN_DB_VIEW = 'Tableau Report Config'

# Functions
"TBD Scanner"
"Lotus connector import"
db = connect(LN_KEY, LN_SERVER_NAME, LN_DB_NAME)

for view in list_views(db):
	print(view.Name)
	for doc in list_documents(view):
		describe_document(doc)
	





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