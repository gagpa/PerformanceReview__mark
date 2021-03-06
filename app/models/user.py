from datetime import datetime

from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    """ Модель пользователя """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    username = Column(VARCHAR(50), unique=True, nullable=False)
    fullname = Column(VARCHAR(255), nullable=False)
    chat_id = Column(VARCHAR(25), unique=True, nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    boss_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    role_id = Column(SmallInteger, ForeignKey('roles.id'), nullable=False)
    position_id = Column(SmallInteger, ForeignKey('positions.id'), nullable=False)

    boss = relationship('User', backref='staff', remote_side=id)
    department = relationship('Department', backref='users')
    role = relationship('Role', backref='users')
    position = relationship('Position', backref='users')

    __mapper_args__ = {
        'order_by': id
    }

    def __repr__(self):
        return f'User: {self.username} {self.chat_id}'


__all__ = ['User']
