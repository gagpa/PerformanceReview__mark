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
    hr_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    hr_review_status_id = Column(Integer, ForeignKey('hr_review_statuses.id', ondelete='CASCADE'), nullable=True)
    hr_comment_id = Column(Integer, ForeignKey('hr_comments.id', ondelete='CASCADE'), nullable=True)

    form = relationship('Form', backref='advices')
    coworker = relationship('User', foreign_keys=[user_id], backref='advices')
    hr = relationship('User', foreign_keys=[hr_user_id], backref='advices_on_review')
    hr_review_status = relationship('HrReviewStatus', backref='advices_on_review')
    hr_comment = relationship('HrComment', backref='advices_on_review')

    def __repr__(self):
        return f'CoworkerAdvice'


__all__ = ['CoworkerAdvice']
