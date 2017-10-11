from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymssql

def dict_attributes(dict_list):
    "return dictionaries attributes required to generate table schema"
    fields_dict = {}
    fields = list(set().union(*(dict.keys() for dict in dict_list))) #create a unique set of all dict keys
    fields.sort()
    for field in fields:
        max_val = []
        for dict in dict_list:
            if field in dict:
                max_val.append(len(dict[field]))
        fields_dict[field] = max(max(max_val),1) # give field length a minimum of 1 or it defaults to MAX when assigned as a column
    return fields_dict


def connect(host,dbname,user,password,port=1433,driver='mssql+pymssql'): #1433 is default MSSQL port
    "Helper function for creating MSSQL db connection"
    #'driver://user:password@hostname:port/database_name'
    engine = create_engine('{}://{}:{}@{}:{}/{}'.format(driver,user,password,host,port,dbname))
    conn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session() # I wonder if we can collapse these using a Lambda
    return conn,session,engine

def create_schema(tablename,dict_list): #TODO figure out how to sort columns - ordered dicts etc. seem to have no effect
    "Create sqlalchemy table from dictionary specified columns"
    fields_dict = dict_attributes(dict_list) #Create a dictionary of the required table attributes - clever but not quite wizardry
    attr_dict = dict(((field,Column(String(fields_dict[field])) ) for field in fields_dict)) #turn each key into a String(varchar) column using the max lengths from fields_dict
    attr_dict['ID'] = Column(Integer, primary_key=True) # add a PK - SQLAlchemy demands this
    attr_dict['__tablename__'] = tablename #tablename assignment is done inside the dictionary
    return attr_dict

def create_table(attr_dict,engine,drop=False): #TODO order the fields
    "Create table from dictionary attributes"
    #Dark, dark SQLAlchemy metaclass magic - taken from http://sparrigan.github.io/sql/sqla/2016/01/03/dynamic-tables.html
    Base = declarative_base() #Required for 'declarative' use of the SQLAlchemy ORM
    GenericTableClass = type('GenericTableClass', (Base,), attr_dict) #Use of Type() to dynamically generate columns. More detail here: http://sahandsaba.com/python-classes-metaclasses.html#metaclasses
    if drop:
        Base.metadata.drop_all(engine) #Drop all tables in the scope of this metadata
    Base.metadata.create_all(engine) #Create all tables in the scope of this metadata
    return GenericTableClass,'Table {} successfully created'.format(attr_dict['__tablename__'])


