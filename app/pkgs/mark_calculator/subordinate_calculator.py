import typing
from statistics import mean

from app.db import Session
from app.models import Form, User, Project, CoworkerProjectRating, CoworkerReview
from .base import Calculator


class SubordinateCalculator(Calculator):

    @classmethod
    def calculate(cls, form: Form) -> float:
        return cls._calculate(cls._find_marks(form))

    @classmethod
    def _calculate(cls, marks: typing.List[int]) -> float:
        if marks:
            return round(mean(marks), 2)
        return 0

    @classmethod
    def _find_marks(cls, form: Form):
        projects_comments = Session().query(CoworkerProjectRating) \
            .join(Project, CoworkerProjectRating.project) \
            .join(Form, Project.form) \
            .join(CoworkerReview, CoworkerReview.id == CoworkerProjectRating.coworker_review_id) \
            .join(User, CoworkerReview.coworker)
        subordinate_comments = projects_comments.filter(Form.id == form.id) \
            .filter(User.boss_id == form.user.id).all()
        return [item.rating.value for item in subordinate_comments if item.rating and item.rating.value]
