from sqlalchemy import Column, VARCHAR, Integer, TIMESTAMP

from app.db import base


class Position(base):
    """
    Модель должности.
    """
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)

    name = Column(VARCHAR(50), nullable=False, unique=True)

    def __repr__(self):
        return f'Position {self.name}'
