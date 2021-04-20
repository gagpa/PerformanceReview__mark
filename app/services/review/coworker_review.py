from app.models import CoworkerReview, CoworkerProjectRating
from app.services.abc_entity import Entity
from app.services.dictinary import HrReviewStatusService
from app.db import Session


class CoworkerReviewService(Entity):
    """ Серивис boss review """
    Model = CoworkerReview

    @property
    def is_on_review(self):
        if not self.model.hr_status or self.model.hr_status == HrReviewStatusService().coworker:
            return True
        return False

    def up(self, **kwargs):
        """ Повыись статус """
        if kwargs.get('pk'):
            self.by_pk(kwargs['pk'])
        elif kwargs.get('review'):
            self.model = kwargs['review']
        if self.model:
            self.model.hr_status = HrReviewStatusService().hr
            Session().add(self.model)
            Session.commit()

    def rating_by_pk(self, pk: int):
        """ Вернуть рйтинг по pk """
        return Session().query(CoworkerProjectRating).filter(CoworkerProjectRating.id == pk).first()
