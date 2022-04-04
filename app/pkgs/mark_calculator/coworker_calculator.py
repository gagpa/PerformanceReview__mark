import typing
from statistics import mean

from sqlalchemy import or_

from app.db import Session
from app.models import Form, User, Project, CoworkerProjectRating, CoworkerReview
from .base import Calculator
from app.queries import find__coworkers_marks


class CoworkerCalculator(Calculator):

    @classmethod
    def calculate(cls, form: Form) -> float:
        return cls._calculate(cls._find_marks(form))

    @classmethod
    def _calculate(cls, marks: typing.List[int]) -> float:
        marks = [mark for mark in marks if mark > 0]
        if marks:
            return round(mean(marks), 2)
        return 0

    @classmethod
    def _find_marks(cls, form: Form):
        coworkers_comments = find__coworkers_marks(form).all()
        return [item.rating.value for item in coworkers_comments if item.rating and item.rating.value]
