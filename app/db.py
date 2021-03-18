from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs.db_config import DATABASE_URI

base = declarative_base()

engine = create_engine(DATABASE_URI)

# Импорт необходим для создания новых миграций.
from app.models import *

session_maker = sessionmaker(bind=engine, autoflush=False)
db_session = session_maker()
