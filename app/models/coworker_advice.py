from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP, SmallInteger
from sqlalchemy.orm import relationship, backref
from app.db import Base


class CoworkerAdvice(Base):
    """ Модель комментария """
    __tablename__ = 'coworker_advices'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(1000), nullable=True)
    hr_comment = Column(VARCHAR(1000), nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    coworker_review_id = Column(Integer, ForeignKey('coworker_reviews.id', ondelete='CASCADE'), nullable=False)
    advice_type_id = Column(SmallInteger, ForeignKey('advice_types.id'), nullable=False)

    coworker_review = relationship('CoworkerReview', backref=backref('advices', cascade='all, delete'))
    advice_type = relationship('AdviceType', backref='advices')

    __mapper_args__ = {
        'order_by': id
    }

    def __repr__(self):
        return f'CoworkerAdvice'


__all__ = ['CoworkerAdvice']
