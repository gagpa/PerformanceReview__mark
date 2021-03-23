from app.db import db_session
from app.models import Status, Form


def get_new_form():
    """
    Вернуть статус для новой формы.
    :return:
    """
    status = db_session.query(Status).filter_by(name='Заполнение анкеты').first()
    return status


def get_boss_review():
    """

    :return:
    """
    status = db_session.query(Status).filter_by(name='У руководителя').first()
    return status


def get_emp_review():
    """

    :return:
    """
    status = db_session.query(Status).filter_by(name='На оценке коллег').first()
    return status


def change_boss_review(form: Form):
    """
    Сменить статус на проверке у руководителя.
    :return:
    """
    form.status = get_boss_review()
    db_session.add(form)
    db_session.commit()


def change_emp_review(form: Form):
    """
    Сменить статус на оценка коллег.
    :param form:
    :return:
    """
    form.status = get_emp_review()
    db_session.add(form)
    db_session.commit()


def change_fill_form(form: Form):
    """
    Сменить статус на заполнение формы.
    :param form:
    :return:
    """
    form.status = get_new_form()
    db_session.add(form)
    db_session.commit()
