from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload

from app.db import Session
from app.models import CoworkerAdvice, HrComment, ProjectComment
from app.services.dictinary import HrReviewStatusService, StatusService
from app.services.user.user import UserService


class HRService(UserService):
    """ Сервис сотрудника """

    def advices_on_review(self, is_asc=False):
        order_func = asc if is_asc else desc
        status = HrReviewStatusService().not_reviewed
        advices = Session.query(CoworkerAdvice) \
            .options(joinedload(CoworkerAdvice.form)) \
            .filter(CoworkerAdvice.hr_review_status == status).order_by(order_func(CoworkerAdvice.updated_at)) \
            .all()
        return advices

    def comment_on(self, model, text):
        """ Добавить комментарий """
        if model.hr_comment:
            model.hr_comment.text = text
        else:
            model.hr_comment = HrComment(text=text)
        self.save_all(model)

    def comment_rating(self, pk: int, text: str):
        """ Прокомментировать оценку """
        rating = Session.query(ProjectComment).filter_by(id=pk).first()
        if rating.hr_comment:
            rating.hr_comment.text = text
        else:
            rating.hr_comment = HrComment(text=text)
        self.save_all(rating)

    def accept_coworker_review(self, advice, ratings: list):
        hr_status = HrReviewStatusService().accept
        form_status = StatusService().review_done
        advice.hr_review_status = hr_status
        for rating in ratings:
            rating.hr_review_status = hr_status
        advice.form.status = form_status
        self.save_all(advice, *ratings)
        Session.commit()

    def decline_coworker_review(self, advice, ratings: list):
        hr_status = HrReviewStatusService().reform
        advice.hr_review_status = hr_status
        for rating in ratings:
            rating.hr_review_status = hr_status
        self.save_all(advice, *ratings)
        Session.commit()


__all__ = ['HRService']
