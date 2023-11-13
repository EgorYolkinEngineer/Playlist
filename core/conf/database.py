from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///database.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


