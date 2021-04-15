from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from app.db import Base


class ProjectComment(Base):
    """ Модель """
    __tablename__ = 'projects_comments'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(1000), nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    rating_id = Column(Integer, ForeignKey('ratings.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # hr_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    hr_review_status_id = Column(Integer, ForeignKey('hr_review_statuses.id', ondelete='CASCADE'), nullable=True)
    hr_comment_id = Column(Integer, ForeignKey('hr_comments.id', ondelete='CASCADE'), nullable=True)

    user = relationship('User', foreign_keys=[user_id], backref='projects_comments')
    rating = relationship('Rating', backref='projects_comments')
    project = relationship('Project', backref='comments')
    # hr = relationship('User', foreign_keys=[hr_user_id])
    hr_review_status = relationship('HrReviewStatus', backref='ratings')
    hr_comment = relationship('HrComment', backref='ratings')

    def __repr__(self):
        return f'ProjectComment {self.text} {self.rating}'


__all__ = ['ProjectComment']
