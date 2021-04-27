from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, VARCHAR
from sqlalchemy.orm import relationship

from app.db import Base


class UserHistory(Base):
    """ Модель формы заполнения """
    __tablename__ = 'users_history'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(50), nullable=False)
    url_type = Column(VARCHAR(25), nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', backref='history')

    def __repr__(self):
        return f'UserHistory {self.user} Previous {self.url_type} - {self.text}'


__all__ = ['UserHistory']
