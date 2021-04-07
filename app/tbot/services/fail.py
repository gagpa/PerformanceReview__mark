from app.services.form_review import FailService
from app.tbot.services import AchievementServiceTBot
from app.models import Fail


class FailServiceTBot(AchievementServiceTBot, FailService):
    """  """
    Model = Fail


__all__ = ['FailServiceTBot']
