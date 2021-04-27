from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from app.db import Base


class Summary(Base):
    """ Модель итогов """
    __tablename__ = 'summaries'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(1000), nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    form_id = Column(Integer, ForeignKey('forms.id', ondelete='CASCADE'), nullable=False)
    from_hr_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    form = relationship('Form', backref=backref('summaries', cascade='all, delete-orphan'))
    users = relationship('User', backref=backref('summaries', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'Summary :{self.text}'


__all__ = ['Summary']
