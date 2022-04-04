from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.orm import relationship

from app.db import Base
from app.models.department_position import DepartmentPosition


class Department(Base):
    """ Модель отдела """
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)

    name = Column(VARCHAR(255), nullable=False, unique=True)
    positions = relationship("Position",
                             secondary='departments_positions',
                             backref="departments")

    def __repr__(self):
        return f'Department {self.name}'


__all__ = ['Department']
