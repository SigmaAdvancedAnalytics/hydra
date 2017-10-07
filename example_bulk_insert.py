import sqlalchemy
from sqlalchemy import create_engine,Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd


# Set up of the engine to connect to the database
# the urlquote is used for passing the password which might contain special characters such as "/"
engine = create_engine('mysql://root:%s@localhost/db1' % urlquote('weirdPassword*withsp€cialcharacters'), echo=False)
conn = engine.connect()
Base = declarative_base()

#Declaration of the class in order to write into the database. This structure is standard and should align with SQLAlchemy's doc.
class Current(Base):
    __tablename__ = 'tableName'

    id = Column(Integer, primary_key=True)
    Date = Column(String(500))
    Type = Column(String(500))
    Value = Column(Numeric())

    def __repr__(self):
        return "(id='%s', Date='%s', Type='%s', Value='%s')" % (self.id, self.Date, self.Type, self.Value)

# Set up of the table in db and the file to import
fileToRead = 'file.csv'
tableToWriteTo = 'tableName'

# Panda to create a lovely dataframe
df_to_be_written = pd.read_csv(fileToRead)
# The orient='records' is the key of this, it allows to align with the format mentioned in the doc to insert in bulks.
listToWrite = df_to_be_written.to_dict(orient='records')

metadata = sqlalchemy.schema.MetaData(bind=engine,reflect=True)
table = sqlalchemy.Table(tableToWriteTo, metadata, autoload=True)

# Open the session
Session = sessionmaker(bind=engine)
session = Session()

# Inser the dataframe into the database in one bulk
conn.execute(table.insert(), listToWrite)

# Commit the changes
session.commit()

# Close the session
session.close()