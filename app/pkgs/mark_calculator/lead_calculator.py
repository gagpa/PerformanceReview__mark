import typing
from statistics import mean

from app.db import Session
from app.models import Form, User, Project, CoworkerProjectRating, CoworkerReview
from .base import Calculator
from app.queries import find__lead_marks

class LeadCalculator(Calculator):

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
        boss_comments = find__lead_marks(form).all()
        return [item.rating.value for item in boss_comments if item.rating and item.rating.value]
