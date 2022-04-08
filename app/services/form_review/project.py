from typing import List

from app.db import Session
from app.models import Project, User, CoworkerReview, CoworkerProjectRating
from app.services.abc_entity import Entity
from app.services.dictinary import HrReviewStatusService
from configs.bot_config import MAX_USERS_ON_PROJECT


class ProjectsService(Entity):
    """ Сервис проектво """
    Model = Project
    model = None
    form = None
    REQUIREMENTS = {}

    @classmethod
    def create_empty(cls, form):
        return Project(form=form)

    @property
    def all_text(self) -> list:
        """ """
        models = self.all
        all_text = [model.text for model in models]
        return all_text

    @property
    def all(self) -> list:
        """  """
        models = Session.query(self.Model).filter_by(form=self.form).all()
        return models

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, text):
        self.model.name = text

    @property
    def description(self):
        return self.model.name

    @description.setter
    def description(self, text):
        self.model.description = text

    @property
    def contacts(self):
        return [review.coworker for review in self.model.reviews]

    def add_contacts(self, contacts: List[str]):
        """ Добавить контакты """
        if not Session.object_session(self.model):
            self.model = Session().merge(self.model)
        self.save_all(self.model)
        users = Session().query(User).filter(User.username.in_(contacts)).all()
        form = self.model.form
        hr_status = HrReviewStatusService().coworker
        i = Session().query(CoworkerProjectRating).filter(CoworkerProjectRating.project_id == self.model.id).count()
        for user in users:
            if i >= MAX_USERS_ON_PROJECT and user.id != form.user.boss_id:
                break
            if user == form.user:
                continue
            i += 1
            reviews = user.coworker_reviews
            review = list(filter(lambda coworker_review: coworker_review.form == form, reviews))
            if review:
                if self.model in review[0].projects:
                    continue
                proj_rating = CoworkerProjectRating(coworker_review=review[0], project=self.model)
                self.save_all(proj_rating)
            else:
                review = CoworkerReview(coworker=user, hr_status=hr_status, form=form)
                proj_rating = CoworkerProjectRating(coworker_review=review, project=self.model)
                self.save_all(review, proj_rating)
        Session().commit()

    def del_contact(self, contact: User):
        """ Удалить контакт из проекта """
        if not Session.object_session(self.model):
            self.model = Session().merge(self.model)
        ratings = Session().query(CoworkerProjectRating). \
            join(CoworkerReview). \
            filter(CoworkerReview.coworker == contact,
                   CoworkerReview.form == self.model.form).all()
        if len(ratings) == 1:
            ratings = ratings[0]
            Session().delete(ratings)
            Session().delete(ratings.coworker_review)
        elif len(ratings) > 1:
            for rate in ratings:
                if rate.project == self.model:
                    Session().delete(rate)
        elif len(ratings) == 0:
            review = Session().query(CoworkerReview).filter(CoworkerReview.coworker == contact, CoworkerReview.form == self.model.form).one()
            Session().delete(review)
        Session.commit()

    def update_contacts(self, old_contact: User, new_contact: User):
        """ Изменить контакт в проекте """
        if not Session.object_session(self.model):
            self.model = Session().merge(self.model)
        is_exist = Session().query(CoworkerReview). \
            join(CoworkerProjectRating). \
            filter(CoworkerProjectRating.project == self.model,
                   CoworkerReview.coworker == new_contact). \
            first()
        if not is_exist:
            review = Session().query(CoworkerReview). \
                join(CoworkerProjectRating). \
                filter(CoworkerProjectRating.project == self.model,
                       CoworkerReview.coworker == old_contact). \
                first()
            review.coworker = new_contact
            Session().add(review)
            Session.commit()
