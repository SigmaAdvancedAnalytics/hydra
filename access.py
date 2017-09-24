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

session = get_session(ln_key="OldUser34#$") #,workdir=r"C:\Users\jbarber\AppData\Local\IBM\Notes"
db = session.GetDatabase(SERVER_NAME, DB_NAME)

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