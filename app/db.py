from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from configs.db_config import DATABASE_URI

Base = declarative_base()

engine = create_engine(DATABASE_URI)
from app.models import *

# Импорт необходим для создания новых миграций.

SessionFactory = sessionmaker(bind=engine, autoflush=False)
Session = scoped_session(SessionFactory)

__all__ = ['Base', 'Session']