from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, VARCHAR
from sqlalchemy.orm import relationship, backref

from app.db import Base


class UserHistory(Base):
    """ Модель формы заполнения """
    __tablename__ = 'users_history'
    id = Column(Integer, primary_key=True)

    text = Column(VARCHAR(50), nullable=False)
    url_type = Column(VARCHAR(25), nullable=False)
    args = Column(VARCHAR(100), nullable=True)
    message_id = Column(VARCHAR(50), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', backref=backref('history', cascade='all, delete'))

    __mapper_args__ = {
        'order_by': id
    }

    def __repr__(self):
        return f'UserHistory {self.user} Previous {self.url_type} - {self.text}'


__all__ = ['UserHistory']
