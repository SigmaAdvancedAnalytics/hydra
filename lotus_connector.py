import datetime
import os
import pickle
import pprint as pp
import pywintypes
from win32com.client import Dispatch, makepy

# Update win32com to use the IBM Notes classes
makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
makepy.GenerateFromTypeLibSpec('IBM Notes Automation Classes')


#Database > View > Doc > Item.Values
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


def lndoc2dict(doc):
    "Convert NotesDocument to a Python dictionary"
    vals = []
    if doc.Items:
        for k in doc.Items:
            item = doc.GetFirstItem(k.Name)   
            val = tuple(convert_datetime(i) for i in item.Values)
            r = (k.Name, val)
            vals.append(r)
    return dict(vals)

def pickle_dict(dict,file_loc=None):
    "Save a dictionary into a pickle file"                              "Pickle is serialising the list, not catching the nested dictionaries. Need to either write a helper func, or append each dict to a single file then retrive all as a list"
    file = file_loc+'\pickle.p'
    with open(file, "wb") as f:
        pickle.dump(dict, f)


# inline execution as 32-bit python cannot be run from py3 main.py
# Lotus credentials
# Python 2 C:\Users\jbarber\AppData\Local\Programs\Python\Python36-32\ python
LN_KEY = "OldUser34#$" #Todo: convert these into a .env file
LN_SERVER = 'Toronto16/BASFPro'
LN_DB = r"BASF\agprocan\agcreports.nsf"
LN_VIEW = 'Tableau Report Config'


#connect to lotus db
print('Connecting to {0}\{1}'.format(LN_SERVER,LN_DB))
db = connect(LN_KEY, LN_SERVER, LN_DB)

#extract lotus documents as a list of dictionaries
print('Extracting documents from view {0}'.format(LN_VIEW))
lotus_docs = []

target_view = get_view(db,LN_VIEW)
for doc in list_documents(target_view):
    doc_dict = lndoc2dict(doc)
    print(doc_dict)
    lotus_docs.extend(doc_dict)
print("Extracted {0} Lotus documents.".format(len(lotus_docs)))
print(lotus_docs)
#pp.pprint(lotus_docs)


#pickle dict
script_loc = os.path.dirname(os.path.realpath(__file__))
print('Writing to pickle file in {0}.'.format(script_loc))
pickle_dict(lotus_docs,script_loc)
print('Pickle complete')

# load pickle dict
lotus_docs = pickle.load( open( script_loc+"/pickle.p", "rb" ) )
print(lotus_docs)