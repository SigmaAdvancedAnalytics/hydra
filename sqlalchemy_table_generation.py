# Test implementation of dynamic table generation using SQL Alchemy ORM capabilities
# Taken from http://sparrigan.github.io/sql/sqla/2016/01/03/dynamic-tables.html
import sqlalchemy

SERVER_NAME = ''
DATABASE_NAME = ''

#Establish windows authenticated session - Not yet tested
engine = sqlalchemy.create_engine('mssql://'+SERVER_NAME+'/'+DATABASE_NAME+'?trusted_connection=yes')

#Required for 'declarative' use of the SQLAlchemy ORM
Base = declarative_base()

#Use of Type() to dynamically generate columns. More detail here: http://sahandsaba.com/python-classes-metaclasses.html#metaclasses
attr_dict = {'__tablename__': 'Lotus_Test',
	     'myFirstCol': Column(Integer, primary_key=True),
	     'mySecondCol': Column(Integer)}
#Create table from dictionary specified columns
MyTableClass = type('MyTableClass', (Base,), attr_dict)
Base.metadata.create_table(engine)

# Dynamic insert using Dictionary unpacking
firstColName = "Ill_decide_later"
secondColName = "Seriously_quit_bugging_me"

new_row_vals = MyTableClass(**{firstColName: 14, secondColName: 33})



""" Reference examples of the original SQLAlchemy syntax

#Table creation
	#Required for 'declarative' use of the SQLAlchemy ORM
	Base = declarative_base()

	#Explicitly defined columns example
	class MyTableClass(Base):
		__tablename__ = 'Test_table'
		myFirstCol = Column(Integer, primary_key=True)
		mySecondCol = Column(Integer, primary_key=True)
	Base.metadata.create_table(engine)

# Row insertion
	new_row_vals = MyTableClass(myFirstCol=14, mySecondCol=33)

	session.add(new_row_vals) # Add to session
	session.commit() # Commit everything in session

# Specify columns for insertion
	firstColName = "Ill_decide_later"
	secondColName = "Seriously_quit_bugging_me"

	new_row_vals = MyTableClass(firstColName=14, secondColName=33)


"""