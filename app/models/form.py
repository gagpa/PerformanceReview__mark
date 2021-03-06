from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, SmallInteger, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db import base


class Form(base):
    """
    Модель формы заполнения.
    """
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    review_period_id = Column(Integer, ForeignKey('review_periods.id'), nullable=False)
    rating_id = Column(SmallInteger, ForeignKey('ratings.id'))  # TODO  разобраться с рейтингом
    status_id = Column(SmallInteger, ForeignKey('statuses.id'), nullable=False)

    user = relationship('User', backref='forms')
    review_period = relationship('ReviewPeriod', backref='forms')
    rating = relationship('Rating', backref='forms')
    status = relationship('Status', backref='forms')

    def __repr__(self):
        return f'Form user'
