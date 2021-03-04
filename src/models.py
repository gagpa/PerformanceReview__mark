from sqlalchemy import Column, Text, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import SQLALCHEMY_DATABASE_URI

base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI)
base.metadata.create_all(engine)

session_maker = sessionmaker(bind=engine)
db_session = session_maker()


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(Text)
    position = Column(Text)
    department = Column(Text)
    chef = Column(Text)
    username = Column(Text, unique=True)
    roles = Column(Text)

    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def lookup(cls, id):
        return db_session.query(User).filter_by(id=id).one_or_none()

    @classmethod
    def update(cls, id, **kwargs):
        return db_session.query(User).filter_by(id=id).update({**kwargs})

    @classmethod
    def identify(cls, id):
        return db_session.query(User).get(id)

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []
