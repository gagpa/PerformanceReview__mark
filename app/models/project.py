from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db import base


class Project(base):
    """
    Модель проекта.
    """
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)

    name = Column(VARCHAR(1000), nullable=False)
    description = Column(VARCHAR(2000), nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    form_id = Column(Integer, ForeignKey('forms.id', ondelete='CASCADE'), nullable=False)

    form = relationship('Form', backref='projects')
    users = relationship('User', secondary='comments')

    def __repr__(self):
        return f'Project :{self.name}'
