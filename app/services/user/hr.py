from app.services.user.user import UserService
from app.services.dictinary import HrReviewStatusService
from app.db import Session
from sqlalchemy.orm import lazyload, joinedload
from app.models import Form, CoworkerAdvice, HrComment


class HRService(UserService):
    """ Сервис сотрудника """

    @property
    def advices_on_review(self):
        status = HrReviewStatusService().not_reviewed
        advices = Session.query(CoworkerAdvice)\
            .options(joinedload(CoworkerAdvice.form))\
            .filter(CoworkerAdvice.hr_review_status == status)\
            .all()
        return advices

    def comment_on(self, model, text):
        """ Добавить комментарий """
        if model.hr_comment:
            model.hr_comment.text = text
        else:
            model.hr_comment = HrComment(text=text)
        self.save_all(model)


__all__ = ['HRService']
