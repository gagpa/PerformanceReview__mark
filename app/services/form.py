from app.db import db_session
from app.models import Form, User, ReviewPeriod, Status, Rating
from app.services.status import get_boss_review


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


def save(form: Form):
    """
    Сохранить
    :param form:
    :return:
    """
    db_session.add(form)
    db_session.commit()


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
    save(form)
    return form


def update_status(form: Form, status: Status):
    """
    Обновить статус формы.
    :param form:
    :param status:
    :return:
    """
    form.status = status
    save(form)


def get(user, review_period: ReviewPeriod) -> Form:
    """

    :param user:
    :param review_period:
    :return:
    """
    form = db_session.query(Form).filter_by(user=user).first()
    return form


def get_on_boss_review(user, review_period: ReviewPeriod):
    """
    :param user:
    :param review_period:
    :return:
    """
    status = get_boss_review()
    data = db_session.query(Form, User, ReviewPeriod, Status).filter_by(user=user, review_period=review_period, status=status).first()
    if data:
        return data[0]


def get_by_id(pk: int):
    """

    :param pk:
    :return:
    """
    form = db_session.query(Form).filter_by(id=pk).first()
    return form
