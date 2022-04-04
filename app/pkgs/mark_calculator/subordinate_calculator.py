import typing
from statistics import mean

from app.models import Form
from app.queries import find__subordinates_marks
from .base import Calculator


class SubordinateCalculator(Calculator):

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
        subordinate_comments = find__subordinates_marks(form).all()
        return [item.rating.value for item in subordinate_comments if item.rating and item.rating.value]
