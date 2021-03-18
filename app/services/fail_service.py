from app.db import db_session
from app.models import Fail, Form


def save(fail: Fail):
    db_session.add(fail)
    db_session.commit()


def create_empty(form: Form):
    """

    :param form:
    :return:
    """
    return Fail(form=form)


def delete(fail: Fail):
    """
    Создать достижение за текущее review.
    """
    db_session.delete(fail)
    db_session.commit()


def is_exist(form) -> bool:
    """
    Проверить существование достижения.
    :param form:
    :return:
    """
    answer = db_session.query(db_session.query(Fail).filter(Fail.form == form).exists()).scalar()
    return answer


def get_all_text(form) -> list:
    """
    Вернуть достижения пользователя.
    :param form:
    :return:
    """
    fails = get_all_in_form(form=form)
    fails = [fail.text for fail in fails]
    return fails


def get_all_in_form(form) -> list:
    fails = db_session.query(Fail).filter_by(form=form).all()
    return fails


def get_for_pk(pk: int) -> Fail:
    """

    :param pk:
    :return:
    """
    fail = db_session.query(Fail).filter_by(id=pk).first()
    return fail
