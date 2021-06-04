from sqlalchemy import Column, SmallInteger, VARCHAR

from app.db import Base


class AdviceType(Base):
    """ Тип совета"""
    __tablename__ = 'advice_types'
    id = Column(SmallInteger, primary_key=True)

    name = Column(VARCHAR(50), unique=True, nullable=False)

    def __repr__(self):
        return f'AdviceType - {self.name}'
