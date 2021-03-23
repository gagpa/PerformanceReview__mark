from sqlalchemy import Column, VARCHAR, Integer

from app.db import base


class Role(base):
    """ Модель ролей """
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)

    name = Column(VARCHAR(25), nullable=False, unique=True)

    def __repr__(self):
        return f'Role {self.name}'


__all__ = ['Role']
