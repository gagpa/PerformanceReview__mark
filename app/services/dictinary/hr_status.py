from app.models import HrReviewStatus
from app.services.abc_entity import Entity


class HrReviewStatusService(Entity):
    """ Сущность оценки """
    Model = HrReviewStatus

    @property
    def not_reviewed(self):
        return self.by(name='Не проверяна')

    @property
    def reform(self):
        return self.by(name='На исправление')

    @property
    def after_reform(self):
        return self.by(name='После исправления')

    @property
    def accept(self):
        return self.by(name='Принята')
