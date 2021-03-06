from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from app.db import Base


class CoworkerProjectRating(Base):
    """ Модель """
    __tablename__ = 'coworker_project_ratings'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(1000), nullable=True)
    hr_comment = Column(VARCHAR(1000), nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    rating_id = Column(Integer, ForeignKey('ratings.id'), nullable=True)
    coworker_review_id = Column(Integer, ForeignKey('coworker_reviews.id', ondelete='CASCADE'), nullable=False)

    project = relationship('Project', uselist=False, backref=backref('ratings', cascade='all, delete'))
    coworker_review = relationship('CoworkerReview',
                                   backref=backref('coworker_project_rating', cascade='all, delete'))
    rating = relationship('Rating', backref='projects_comments')

    __mapper_args__ = {
        'order_by': id
    }

    def __repr__(self):
        return f'ProjectComment {self.text} {self.rating}'


__all__ = ['CoworkerProjectRating']
