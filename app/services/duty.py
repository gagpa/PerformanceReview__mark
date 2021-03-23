from app.db import db_session
from app.models import Duty, Form


def add(text, form):
    """
    Добавить обязанность в форму.
    :param text:
    :param form:
    :return:
    """
    duty_model = Duty(text=text, form=form)
    db_session.add(duty_model)
    db_session.commit()
    return duty_model


def edit(text, form):
    """
    Изменить обязанность в форме.
    :param text:
    :param form:
    :return:
    """
    duty_model = db_session.query(Duty).filter_by(form=form).first()
    duty_model.text = text
    db_session.add(duty_model)
    db_session.commit()
    return duty_model


def update(form: Form, duty: str):
    """

    :param form:
    :param duty:
    :return:
    """
    if is_exist(form):
        duty_model = db_session.query(Duty).filter_by(form_id=form).first()
        duty_model.text = duty
    else:
        raise


def is_exist(form: Form) -> bool:
    """
    Проверить существование обязанности в форме.
    :param form:
    :return:
    """
    answer = db_session.query(db_session.query(Duty).filter(Duty.form == form).exists()).scalar()
    return answer


def get(form: Form) -> Duty:
    """
    Вернуть текст обязанности.
    :param form:
    :return:
    """
    duty = db_session.query(Duty).filter(Duty.form == form).first()
    return duty
