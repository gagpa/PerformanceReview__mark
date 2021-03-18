from app.db import db_session
from app.models import Form, User, ReviewPeriod, Status, Rating


def is_exist(user: User, review_period: ReviewPeriod) -> bool:
    """
    Проверка существование формы.
    :param user:
    :param review_period:
    :return:
    """
    answer = db_session.query(db_session.query(Form).
                              filter_by(user=user, review_period=review_period).
                              exists()).scalar()
    return answer


def create(user: User, review_period: ReviewPeriod, status: Status, rating: Rating = None):
    """
    Создание формы.
    :param user:
    :param review_period:
    :param status:
    :param rating:
    :return:
    """
    form = Form(user=user, review_period=review_period, status=status)
    db_session.add(form)
    db_session.commit()
    return form


def update_status(form: Form, status: Status):
    """
    Обновить статус формы.
    :param form:
    :param status:
    :return:
    """
    form.status = status
    db_session.add(form)
    db_session.commit()


def get(user, review_period: ReviewPeriod) -> Form:
    """

    :param user:
    :param review_period:
    :return:
    """
    form = db_session.query(Form).filter_by(user=user, review_period=review_period).first()
    return form
