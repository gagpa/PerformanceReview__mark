from app.db import db_session
from app.models import Status, Form


def get_new_form():
    """ Вернуть статус для новой формы """
    status = db_session.query(Status).filter_by(name='Заполнение анкеты').first()
    return status


def get_boss_review():
    """ Получить статус на оценке босса """
    status = db_session.query(Status).filter_by(name='У руководителя').first()
    return status


def get_coworker_review():
    """ Получить статус на оценке коллег """
    status = db_session.query(Status).filter_by(name='На оценке коллег').first()
    return status


def change_boss_review(form: Form):
    """ Сменить статус на проверке у руководителя """
    form.status = get_boss_review()
    db_session.add(form)
    db_session.commit()


def change_emp_review(form: Form):
    """ Сменить статус на оценка коллег """
    form.status = get_coworker_review()
    db_session.add(form)
    db_session.commit()


def change_fill_form(form: Form):
    """ Сменить статус на заполнение формы """
    form.status = get_new_form()
    db_session.add(form)
    db_session.commit()


STATUS_BOSS_REVIEW = get_boss_review()

STATUS_COWORKER_REVIEW = get_coworker_review()

STATUS_WRITE_FORM = get_new_form()
