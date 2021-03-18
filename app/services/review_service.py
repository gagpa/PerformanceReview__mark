from app.db import db_session
from app.models import ReviewPeriod


def get_current() -> ReviewPeriod:
    """
    Выдать текущий review период.
    :return:
    """
    period = db_session.query(ReviewPeriod).filter_by(is_active=True).first()
    return period
