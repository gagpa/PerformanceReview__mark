from app.db import Session
from app.models import Form, Project, User, CoworkerReview, CoworkerAdvice, CoworkerProjectRating
from app.services.abc_entity import Entity
from app.services.dictinary import HrReviewStatusService


class ProjectsService(Entity):
    """ Сервис проектво """
    Model = Project
    model = None
    form = None
    REQUIREMENTS = {}

    @classmethod
    def create_empty(cls, form: Form):
        """ """
        return cls.Model(form=form)

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

    @contacts.setter
    def contacts(self, contacts):  # TODO Обдумать .merge()
        contacts = [contact.replace('@', '') for contact in contacts]
        if not Session.object_session(self.model):
            self.model = Session().merge(self.model)
        users = Session().query(User).filter(User.username.in_(contacts)).all()
        form = self.model.form
        hr_status = HrReviewStatusService().coworker
        for user in users:
            reviews = user.coworker_reviews
            if form not in [review.advice.form for review in reviews]:
                review = CoworkerReview(coworker=user, hr_status=hr_status)
                advice = CoworkerAdvice(coworker_review=review, form=form)
                proj_rating = CoworkerProjectRating(review=review, project=self.model)
                self.save_all(review, advice, proj_rating)
            else:
                is_exist = Session().query(Session().query(CoworkerProjectRating).
                                           join(CoworkerReview).
                                           filter(CoworkerReview.coworker == user, CoworkerProjectRating.project == self.model).
                                           exists()).scalar()
                if not is_exist:
                    review = Session().query(CoworkerReview).join(CoworkerAdvice). \
                        filter(CoworkerReview.coworker == user, CoworkerAdvice.form == form).first()
                    proj_rating = CoworkerProjectRating(review=review, project=self.model)
                    self.save_all(proj_rating)
        Session().commit()
