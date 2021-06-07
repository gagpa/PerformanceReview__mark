from app.db import Session
from app.models import CoworkerReview, CoworkerAdvice, Form, CoworkerProjectRating
from app.services.abc_entity import Entity
from app.services.dictinary import HrReviewStatusService


class HrReviewService(Entity):
    """ Серивис boss review """
    Model = CoworkerReview

    @property
    def is_on_review(self):
        return self.model.hr_status == HrReviewStatusService().hr

    def down(self, **kwargs):
        """ Повыись статус """
        if kwargs.get('pk'):
            self.by_pk(kwargs['pk'])
        elif kwargs.get('review'):
            self.model = kwargs['review']
        if self.model:
            self.model.hr_status = HrReviewStatusService().coworker
            Session().add(self.model)
            Session.commit()

    def is_last_review(self, review):
        """ Посмотреть все закончили комментирвоать форму """
        status = HrReviewStatusService().coworker
        reviews = Session().query(CoworkerReview).join(Form). \
            filter(CoworkerReview.hr_status == status,
                   CoworkerReview.form == review.form
                   ).all()

        if reviews:
            return False
        return True

    @staticmethod
    def not_rated(form_id):
        """ Посмотреть всех, кто не оценил форму """
        reviews = Session().query(CoworkerReview).join(CoworkerAdvice). \
            join(CoworkerProjectRating). \
            filter(CoworkerProjectRating.rating_id == None,
                   CoworkerAdvice.form_id == form_id
                   ).all()

        users = [f'{i+1}. @{review.coworker.username}' for i, review in enumerate(reviews)]
        return users
