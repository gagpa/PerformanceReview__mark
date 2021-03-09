from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP

from app.db import base


class Comment(base):
    """
    Модель комментария.
    """
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(255), nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Comment'
