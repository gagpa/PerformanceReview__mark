from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, SmallInteger
from sqlalchemy.orm import relationship, backref

from app.db import Base


class CoworkerReview(Base):
    """ Модель проверки босса """
    __tablename__ = 'coworker_reviews'
    id = Column(Integer, primary_key=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    hr_status_id = Column(SmallInteger, ForeignKey('hr_review_statuses.id'), nullable=True)
    coworker_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    form_id = Column(Integer, ForeignKey('forms.id', ondelete='CASCADE'), nullable=False)

    hr_status = relationship('HrReviewStatus', backref='coworker_reviews')
    coworker = relationship('User', backref=backref('coworker_reviews', cascade='all, delete'))
    projects = relationship('Project', secondary='coworker_project_ratings')
    projects_ratings = relationship('CoworkerProjectRating', backref=backref('review', uselist=False))
    form = relationship('Form', backref=backref('coworker_reviews', cascade='all, delete'))

    __mapper_args__ = {
        'order_by': id
    }

    def __repr__(self):
        return f'CoworkerReview {self.coworker} - {self.form.user}'


__all__ = ['CoworkerReview']
