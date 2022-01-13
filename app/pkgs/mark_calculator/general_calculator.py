import typing
from statistics import mean

from app.models import Form
from .base import Calculator
from .coworker_calculator import CoworkerCalculator
from .lead_calculator import LeadCalculator
from .subordinate_calculator import SubordinateCalculator


class GeneralCalculator(Calculator):

    @classmethod
    def calculate(cls, form: Form) -> float:
        return cls._calculate(cls._find_marks(form))

    @classmethod
    def _calculate(cls, marks: typing.List[float]) -> float:
        marks = [mark for mark in marks if mark > 0]
        if marks:
            return round(mean(marks), 2)
        return 0

    @classmethod
    def _find_marks(cls, form: Form) -> typing.List[float]:
        marks = \
            [
                LeadCalculator.calculate(form),
                CoworkerCalculator.calculate(form),
                SubordinateCalculator.calculate(form),
            ]
        return [mark for mark in marks if mark]
