from app.db import Session
from app.models import CoworkerReview
from app.services.abc_entity import Entity
from app.services.dictinary import HrReviewStatusService, StatusService


class HrReviewService(Entity):
    """ Серивис boss review """
    Model = CoworkerReview

    @property
    def is_on_review(self):
        if self.model.hr_status == HrReviewStatusService().hr:
            return True
        return False

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
        form_status = StatusService().review_done
        reviews = Session().query(CoworkerReview).filter(CoworkerReview.hr_status != form_status,
                                                         CoworkerReview.id != review.id,
                                                         ).all()
        if reviews:
            return False
        return True
