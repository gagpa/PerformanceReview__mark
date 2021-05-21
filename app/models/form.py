from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, SmallInteger, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from app.db import Base


class Form(Base):
    """ Модель формы заполнения """
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    review_period_id = Column(Integer, ForeignKey('review_periods.id'), nullable=False)
    status_id = Column(SmallInteger, ForeignKey('statuses.id'), nullable=False)

    user = relationship('User', backref=backref('forms', cascade='all, delete'))
    review_period = relationship('ReviewPeriod', backref='forms')
    status = relationship('Status', backref='forms')

    __mapper_args__ = {
        'order_by': id
    }

    def __repr__(self):
        return f'Form {self.user}'


__all__ = ['Form']
