from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


Base = declarative_base()


# *change username and password according to yours*
hostname = 'localhost'
port = 3306
database = 'product_db'
username = 'root'
password = 'admin'
dburl = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(username, password, hostname, port, database)



engine = create_engine(dburl, echo = True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()