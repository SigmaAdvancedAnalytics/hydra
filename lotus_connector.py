import win32com.client 
import pywintypes
import getpass

SERVER_NAME = 'Toronto16/BASFPro'
DB_NAME = "BASF\\agprocan\\agcreports.nsf"
MY_NOTES_PASSWORD = 'OldUser34#$'

# Initialise Lotus DB connection
#win32com.client.makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
#win32com.client.makepy.GenerateFromTypeLibSpec('IBM Notes Automation Classes')

notesSession = win32com.client.Dispatch('Lotus.NotesSession')
notesSession.Initialize(notesPass)
notesDatabase = notesSession.GetDatabase(notesServer,notesFile)
notesView = '(All Documents)'
"""
session = Dispatch('Lotus.NotesSession')
session.Initialize(MY_NOTES_PASSWORD)

db = session.getDatabase(SERVER_NAME, DB_NAME)
def iterateDocuments(docs):
    doc = docs.getFirstDocument()
    while doc:
        yield doc
        doc = docs.getNextDocument(doc)

for doc in iterateDocuments(view):
        do_something_with(doc)

def get(doc, attr):
    return doc.getItemValue(attr)

def get1(doc, attr):
    return get(doc, attr)[0]
"""