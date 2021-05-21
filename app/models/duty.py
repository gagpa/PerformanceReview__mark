from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from app.db import Base


class Duty(Base):
    """ Модель обязанностей """
    __tablename__ = 'duties'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(1000), nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    form_id = Column(Integer, ForeignKey('forms.id', ondelete='CASCADE'), nullable=False, unique=True)

    form = relationship('Form', backref=backref('duty', uselist=False, cascade='all, delete'))

    __mapper_args__ = {
        'order_by': id
    }

    def __repr__(self):
        return f'Duty {self.text}'


__all__ = ['Duty']
