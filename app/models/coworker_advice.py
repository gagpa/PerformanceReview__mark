from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db import Base


class CoworkerAdvice(Base):
    """ Модель комментария """
    __tablename__ = 'coworker_advices'
    id = Column(Integer, primary_key=True)

    todo = Column(VARCHAR(1000), nullable=True)
    not_todo = Column(VARCHAR(1000), nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    form_id = Column(Integer, ForeignKey('forms.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    coworker = relationship('User', backref='advices')
    form = relationship('Form', backref='advices')

    def __repr__(self):
        return f'CoworkerAdvice'


__all__ = ['CoworkerAdvice']
