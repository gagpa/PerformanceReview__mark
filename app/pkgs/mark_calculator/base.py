from abc import ABC, abstractclassmethod

from app.models import Form


class Calculator(ABC):

    @abstractclassmethod
    def calculate(cls, form: Form) -> float:
        pass
