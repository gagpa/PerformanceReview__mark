from app.models import Role
from app.db import db_session


def get_hr():
    """
    Вернуть роль hr
    :return:
    """
    role = db_session.query(Role).filter_by(name='HR').first()
    return role


def get_employee():
    """
    Вернуть роль сотрудника.
    :return:
    """
    role = db_session.query(Role).filter_by(name='Employee').first()
    return role


def get_lead():
    """
    Вернуть роль руководителя.
    :return:
    """
    role = db_session.query(Role).filter_by(name='Lead').first()
    return role
