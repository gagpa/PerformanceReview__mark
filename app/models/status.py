from sqlalchemy import Column, VARCHAR, SmallInteger

from app.db import Base


class Status(Base):
    """ Модель статуса формы """
    __tablename__ = 'statuses'
    id = Column(SmallInteger, primary_key=True)

    name = Column(VARCHAR(50), unique=True, nullable=False)

    def __repr__(self):
        return f'Status: {self.name}'


__all__ = ['Status']
