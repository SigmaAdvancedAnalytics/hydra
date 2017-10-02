import datetime
import pprint
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


def describe_database(db):
    "Print views with dist doc as example" #db.AllDocuments
    for view in db.Views:
        doc = view.GetFirstDocument()
        print('\nView:', view.Name,'\nFirst document:')
        if doc is not None:
            describe_document(doc)


def describe_view(view):
    "print view information"
    doc = view.GetFirstDocument()
    print('\nView:', view.Name,'\nDocuments:')
    while doc:
        print('\tUID: ',doc.UniversalID,' NotesURL:',doc.NotesURL)
        doc = view.GetNextDocument(doc)


def convert_datetime(obj):
    "convert pywintypes.Time to datetime"
    if type(obj) == pywintypes.TimeType:
        datetime_obj = datetime.datetime(
        year=obj.year,
        month=obj.month,
        day=obj.day,
        hour=obj.hour,
        minute=obj.minute,
        second=obj.second
    )
        return str(datetime_obj)
    else:
        return obj
        

def describe_document(doc):
    "print document information"
    items = []
    for key in doc.Items:
        item = doc.GetFirstItem(key.Name)   
        val = tuple(convert_datetime(i) for i in item.Values)
        r = (item.Name, val)
        items.append(r)
    items.sort()
    print('\t',doc.NotesURL,':')
    for i in items:
        print('\t',i)


def list_views(db):
    "return views in database"
    for view in db.Views:
        yield view


def list_documents(view):
    "return documents in view"
    doc = view.GetFirstDocument()
    while doc:
        yield doc
        doc = view.GetNextDocument(doc)


def get_view(db, view_name):
    "get requested view"
    return db.GetView(view_name)


def get_document(db, view, doc_id):
    "get document with requested UUID"
    doc = view.GetFirstDocument()
    while doc:
        if doc.UniversalID == doc_id:
            return doc
        doc = view.GetNextDocument(doc)


def lndoc2obj(doc):
    "Convert NotesDocument to a Python dictionary"
    vals = []
    if doc.Items:
        for k in doc.Items:
            item = doc.GetFirstItem(k.Name)   
            val = tuple(convert_datetime(i) for i in item.Values)
            r = (k.Name, val)
            vals.append(r)
    return dict(vals)


# function test
# Lotus credentials
LN_KEY = "OldUser34#$" #Todo: convert these into a .env file
LN_SERVER = 'Toronto16/BASFPro'
LN_DB = r"BASF\agprocan\agcreports.nsf"
LN_VIEW = 'Tableau Report Config'

db = connect(LN_KEY, LN_SERVER, LN_DB)
#describe_database(db)
#
#describe_view(target_view)


target_view = get_view(db,LN_VIEW)
for doc in list_documents(target_view):
    #describe_document(doc)
    print('\n')
    pprint.pprint(lndoc2obj(doc))


#target_doc = get_document(db,target_view,'C93625A4F548DD408525816F0055F3A5')
#describe_document(target_doc)



#for doc in list_documents(target_view):
 #   describe_document(doc)

	






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