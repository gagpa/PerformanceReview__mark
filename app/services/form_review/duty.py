from app.models import Duty
from app.services.abc_entity import Entity


class DutyService(Entity):
    """ Сервис обязанностей """
    Model = Duty
