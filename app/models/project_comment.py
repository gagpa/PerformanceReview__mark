from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

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
    user = relationship('User', backref='projects_comments')
    rating = relationship('Rating', backref='projects_comments')
    project = relationship('Project', backref='comments')

    def __repr__(self):
        return f'ProjectComment {self.text} {self.rating}'


__all__ = ['ProjectComment']
