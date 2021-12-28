from app.db import Session
from app.models import ReviewPeriod
from app.services.review import ReviewPeriodService


def send_to_archive():
    """Отправить в архив"""
    for review in Session().query(ReviewPeriod).filter_by(is_active=False).all():
        ReviewPeriodService(review).send_to_archive()
