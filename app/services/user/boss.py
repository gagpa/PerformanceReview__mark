from app.db import Session
from app.models import BossReview, Form, User, ReviewPeriod
from app.services.dictinary.status import StatusService
from app.services.review import ReviewPeriodService
from app.services.user.user import UserService
from app.services.review import BossReviewService


class BossService(UserService):
    """ Сервис началиьника/руководителя """

    def accept(self, form: Form):
        """ Принять """
        StatusService().change_to_coworker_review(form)

    def decline(self, form: Form, text: str) -> BossReview:
        """ Отклонить """
        review_service = BossReviewService()
        if review_service.is_exist(form=form):
            review = review_service.by(form=form)
        else:
            review = review_service.create(form=form)
            review.boss = self.model
        review.text = text
        service = StatusService()
        service.change_to_write_in(form)
        Session().add(review)
        return review

    @property
    def employees(self):
        """ Вернуть всех подчинённых """
        employees = Session.query(User).filter_by(boss=self.model).all()
        return employees

    @property
    def forms_on_review(self):
        """ Вернуть все формы на boss review """
        review_period = ReviewPeriodService().current
        status = StatusService().boss_review
        forms = Session.query(Form).\
            join(User).\
            filter(Form.review_period == review_period,
                   User.boss == self.model,
                   Form.status == status
                   ).all()
        # forms = Session.query(Form).filter(
        #     Form.review_period == review_period,
        #     Form.status == status).all()
        if forms:
            return forms


__all__ = ['BossService']
