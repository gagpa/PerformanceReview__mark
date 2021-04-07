from app.models import ReviewPeriod
from app.services.abc_entity import Entity


class ReviewPeriodService(Entity):
    """  """
    Model = ReviewPeriod

    @property
    def current(self) -> ReviewPeriod:
        """ Выдать текущий review период """
        return self.by(is_active=True)

    @property
    def is_now(self) -> bool:
        """ Ответить проходит сейчас ревью """
        return self.is_exist(is_active=True)


__all__ = ['ReviewPeriodService']
