from app.models import Fail
from app.services.form_review.achievement import AchievementService


class FailService(AchievementService):
    """ Сервис провалов """
    Model = Fail
