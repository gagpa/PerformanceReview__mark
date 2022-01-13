from app.db import Session
from app.models import ReviewPeriod
from app.pkgs.review_archive import ReviewArchive


def send_to_archive():
    """Отправить в архив"""
    for review in Session().query(ReviewPeriod).filter_by(is_active=False).all():
        ReviewArchive().archive_review(review)
