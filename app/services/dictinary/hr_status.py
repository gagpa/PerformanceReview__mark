from app.models import HrReviewStatus
from app.services.abc_entity import Entity


class HrReviewStatusService(Entity):
    """ Сущность оценки """
    Model = HrReviewStatus

    @property
    def hr(self):
        return self.by(name='hr review')

    @property
    def coworker(self):
        return self.by(name='coworker review')

    @property
    def accept(self):
        return self.by(name='accept')
