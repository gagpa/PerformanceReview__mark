from sqlalchemy import Column, VARCHAR, Integer

from app.db import base


class Department(base):
    """
    Модель отдела.
    """
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)

    name = Column(VARCHAR(255), nullable=False, unique=True)

    def __repr__(self):
        return f'Department {self.name}'
