from app.models import BossReview
from app.services.abc_entity import Entity


class BossReviewService(Entity):
    """ Серивис boss review """
    Model = BossReview
