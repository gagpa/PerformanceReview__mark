from sqlalchemy import Column, VARCHAR, Integer

from app.db import Base


class Position(Base):
    """ Модель должности """
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)

    name = Column(VARCHAR(50), nullable=False, unique=True)

    def __repr__(self):
        return f'Position {self.name}'


__all__ = ['Position']
