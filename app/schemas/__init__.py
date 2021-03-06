import typing
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class Relation(Enum):
    lead = 'руководитель'
    coworker = 'коллега'
    subordinates = 'подчинённый'


class Employee(BaseModel):
    """Сотрудник"""
    fullname: str
    department: str
    position: str
    username: str


class EmployeeWithRelation(Employee):
    relation: Relation

    class Config:
        use_enum_values = True


class EmployeeWithLead(Employee):
    """Сотрудник с руководителем"""
    lead: typing.Optional[EmployeeWithRelation]


class ProjectRespondent(BaseModel):
    """Опрошенный сотрудник, по проекту"""
    employee: EmployeeWithRelation
    mark: typing.Optional[int] = Field(None, ge=-1, le=5)
    comment: typing.Optional[str]


class ProjectMark(BaseModel):
    name: str
    description: str
    mark: typing.Optional[int] = Field(None, ge=-1, le=5)
    comment: typing.Optional[str]


class FormRespondent(BaseModel):
    """Опрошенный сотрудник, по анкете"""
    employee: EmployeeWithRelation
    todo: typing.List[str]
    not_todo: typing.List[str]
    marks: typing.List[ProjectMark]
    average_mark: typing.Optional[float]


class Project(BaseModel):
    """Проект сотрудника"""
    name: str
    description: str
    respondents: typing.List[ProjectRespondent]


class Marks(BaseModel):
    """Оценка проекта"""
    lead: typing.Optional[float]
    coworkers: typing.Optional[float]
    subordinates: typing.Optional[float]
    total: typing.Optional[float]


class Summary(BaseModel):
    """Сводная информация по анкете"""
    hr: typing.Optional[Employee]
    text: typing.Optional[str]
    marks: typing.Optional[Marks]


class FormFrame(BaseModel):
    """Анкета из архива"""
    id: typing.Union[UUID, int]
    review: typing.Union[UUID, int]
    author: EmployeeWithLead
    projects: typing.Optional[typing.List[Project]]
    achievements: typing.Optional[typing.List[str]]
    fails: typing.Optional[typing.List[str]]
    duties: typing.Optional[typing.List[str]]
    respondents: typing.Optional[typing.List[FormRespondent]]
    summary: typing.Optional[Summary]
