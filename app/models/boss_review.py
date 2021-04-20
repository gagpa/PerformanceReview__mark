from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from app.db import Base


class BossReview(Base):
    """ Модель проверки босса """
    __tablename__ = 'boss_reviews'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(1000), nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    form_id = Column(Integer, ForeignKey('forms.id', ondelete='CASCADE'), nullable=False)
    boss_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    form = relationship('Form', backref=backref('boss_review', uselist=False))
    boss = relationship('User', backref='boss_reviews')


__all__ = ['BossReview']
