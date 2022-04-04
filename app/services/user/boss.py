from app.db import Session
from app.models import BossReview, Form, User
from app.services.dictinary.status import StatusService
from app.services.form_review.project import ProjectsService
from app.services.review import BossReviewService
from app.services.review import ReviewPeriodService
from app.services.user.user import UserService


class BossService(UserService):
    """ Сервис началиьника/руководителя """

    def accept(self, form: Form):
        """ Принять """
        self.add_in_review(form)
        StatusService().change_to_coworker_review(form)

    def add_in_review(self, form: Form):
        for project in form.projects:
            service = ProjectsService(project)
            service.add_contacts([self.model.username])

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
    def reviews(self):
        """ Вернуть все формы на boss review """
        review_period = ReviewPeriodService().current
        status = StatusService().boss_review
        forms = Session.query(Form). \
            join(User). \
            filter(User.boss == self.model,
                   Form.status == status,
                   Form.review_period == review_period
                   ).all()
        reviews = []
        for form in forms:
            if form.boss_review:
                reviews.append(form.boss_review)
            else:
                review = BossReview(form=form, boss=self.model)
                reviews.append(review)
                Session().add(review)
                Session.commit()
        return reviews


__all__ = ['BossService']
