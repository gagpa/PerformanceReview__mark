from datetime import datetime

from sqlalchemy import Column, VARCHAR, TIMESTAMP, SmallInteger

from app.db import base


class Rating(base):
    """
    Модель рейтинга.
    """
    __tablename__ = 'ratings'
    id = Column(SmallInteger, primary_key=True)

    name = Column(VARCHAR(25), nullable=False, unique=True)
    value = Column(SmallInteger, nullable=False, unique=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    def __repr__(self):
        return f'Rating {self.name} = {self.value}'
