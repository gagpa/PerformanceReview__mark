from app.db import db_session
from app.models import ReviewPeriod


def get_current() -> ReviewPeriod:
    """
    Выдать текущий review период.
    :return:
    """
    period = db_session.query(ReviewPeriod).filter_by(is_active=True).first()
    return period


def is_now() -> bool:
    """
    Ответить проходит сейчас ревью.
    :return:
    """
    answer = db_session.query(db_session.query(ReviewPeriod).filter_by(is_active=True).exists()).scalar()
    return answer
