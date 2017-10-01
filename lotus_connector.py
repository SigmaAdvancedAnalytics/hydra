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


def get_view(db, view_name):
    "list views in database"
    return db.GetView(view_name)


def describe_view(view):
    "describe view and first document"
    doc = view.GetFirstDocument()
    print('View:', view.Name)
    describe_document(doc)


def describe_document(doc):
    "print document information"
    items = []
    for key in doc.Items:
        item = doc.GetFirstItem(key.Name)
        val = doc.GetItemValue(item.Name)
        r = (item.Name, val)
        items.append(r)
    items.sort()
    for i in items:
        print(i)


def lndoc2obj(doc):
    """
    Convert NotesDocument to a Python dictionary-like structure.
    Structure:
        {
            '<first_item_name>': {
                'values': ('<first value>', '<second value>),
                'type': 'TEXT',
                'last_modified': datetime.datetime(2015, 2, 10, 12, 45, 34)
            },
            '<second_item_name>': {
                'values': (datetime.datetime(2015, 2, 1, 0, 0, 0),),
                'type': 'DATETIMES',
                'last_modified': datetime.datetime(2015, 2, 2, 10, 13, 43)
            }
        }
    """
    vals = []
    if doc.Items:
        for k in doc.Items:
            itm = doc.GetFirstItem(k.Name)
            if itm.Type in (ItemType.DATETIMES, ItemType.RFC822Text):
                val = tuple([_dt(i) for i in itm.Values])
            else:
                val = doc.GetItemValue(k.Name)

            r = (k.Name, {
                'values': val,
                'type': ITEM_TYPES[itm.Type],
                'last_modified': _dt(itm.LastModified),
            })
            vals.append(r)
    return dict(vals)


# function test
# Lotus credentials
LN_KEY = "OldUser34#$" #Todo: convert these into a .env file
LN_SERVER = 'Toronto16/BASFPro'
LN_DB = r"BASF\agprocan\agcreports.nsf"
LN_VIEW = 'Tableau Report Config'

# Functions
"TBD Scanner"
"Lotus connector import"
db = connect(LN_KEY, LN_SERVER, LN_DB)
view = get_view(db,LN_VIEW)

describe_view(view)
for doc in list_documents(view):
    print(doc)
	





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