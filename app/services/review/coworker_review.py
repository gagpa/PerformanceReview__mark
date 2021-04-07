from app.models import CoworkerAdvice
from app.services.abc_entity import Entity


class CoworkerReviewService(Entity):
    """ Серивис boss review """
    Model = CoworkerAdvice
