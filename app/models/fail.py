from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db import base


class Fail(base):
    """
    Модель провала.
    """
    __tablename__ = 'fails'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(255), nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=False)

    form_id = Column(Integer, ForeignKey('forms.id'), nullable=False)

    form = relationship('Form', backref='fails')

    def __repr__(self):
        return f'Fail'
