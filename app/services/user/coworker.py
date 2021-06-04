from sqlalchemy import or_

from app.db import Session
from app.models import Form, Rating, CoworkerProjectRating, Project, User, CoworkerAdvice, CoworkerReview
from app.services.dictinary import StatusService, HrReviewStatusService, RatingService
from app.services.review import CoworkerReviewService, ReviewPeriodService
from app.services.user.user import UserService


class CoworkerService(UserService):
    """ Сервис коллеги """

    def send_hr(self, pk_review: int):
        """ Отправить HR """
        review_service = CoworkerReviewService()
        review_service.up(pk=pk_review)

    def give_todo(self, text, form):
        """ Дать совет что делать"""
        service = CoworkerReviewService(todo=text, form=form, coworker=self.model)
        if service.is_exist(form=form, coworker=self.model):
            service.by(form=form, coworker=self.model)
            service.update(todo=text)
        else:
            service.create(todo=text, form=form, coworker=self.model)

    def give_not_todo(self, text, form):
        """ Дать совет что перестать делать"""
        service = CoworkerReviewService(todo=text, form=form, coworker=self.model)
        if service.is_exist(form=form, coworker=self.model):
            service.by(form=form, coworker=self.model)
            service.update(not_todo=text)
        else:
            service.create(not_todo=text, form=form, coworker=self.model)

    def comment_on(self, proj_rate_pk: int, text: str):
        """ Прокомментировать проект """
        rating = CoworkerReviewService().rating_by_pk(proj_rate_pk)
        rating.text = text
        self.save(rating)
        Session.commit()

    def find_advice(self, form):
        """ Найти совет """
        advice = Session().query(CoworkerAdvice).filter_by(form=form, coworker=self.model).first()
        return advice

    def find_project_to_comment(self, form: Form) -> list:
        """ Найти проекты в форме для комментирования """
        projects_in_form = form.projects
        projects_to_comment = list(filter(lambda project: self.model in project.users, projects_in_form))
        return projects_to_comment

    def advice_by_pk(self, pk: int):
        """ Совет по pk """
        return Session().query(CoworkerAdvice).filter(CoworkerAdvice.id == pk).first()

    def find_rating(self, project: Project):
        """ """
        project_comment = Session().query(CoworkerProjectRating).filter_by(project=project, user=self.model).first()
        return project_comment.rating

    def find_comment(self, project: Project):
        """ """
        project_comment = Session().query(CoworkerProjectRating).filter_by(project=project, user=self.model).first()
        return project_comment

    def rate_project(self, project: Project, rating: Rating):
        """ Оценить проект """
        project_comment = Session().query(CoworkerProjectRating).filter_by(project=project, user=self.model).first()
        project_comment.rating = rating
        self.save(project_comment)
        Session.commit()

    def rate(self, proj_rate_pk: int, rate_pk: int):
        """ Оценить проект """
        rating = CoworkerReviewService().rating_by_pk(proj_rate_pk)
        rate = RatingService().by_pk(rate_pk)
        rating.rating = rate
        self.save(rating)
        Session.commit()

    @property
    def reviews(self):
        """ Верунть формы на review """
        form_status = StatusService().coworker_review
        hr_status = HrReviewStatusService().coworker
        review_period = ReviewPeriodService().current
        query = Session.query(CoworkerReview).join(Form, User)
        query = query.filter(CoworkerReview.coworker == self.model,
                             CoworkerReview.hr_status == hr_status,
                             Form.status == form_status,
                             Form.review_period == review_period
                             )
        reviews = query.all()
        return reviews


__all__ = ['CoworkerService']
