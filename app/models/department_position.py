from sqlalchemy import Column, VARCHAR, Integer, ForeignKey

from app.db import Base


class DepartmentPosition(Base):
    """ Модель отдела-должности"""
    __tablename__ = 'departments_positions'
    id = Column(Integer, primary_key=True)

    department_id = Column('department_id', Integer, ForeignKey('departments.id'))
    position_id = Column('position_id', Integer, ForeignKey('positions.id'))

    def __repr__(self):
        return f'Department {self.department_id} - Position {self.position_id}'


__all__ = ['DepartmentPosition']