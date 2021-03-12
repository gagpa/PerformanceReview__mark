import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))

from app.models import *

session_maker = sessionmaker(bind=engine)
db_session = session_maker()
