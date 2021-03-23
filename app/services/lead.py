from app.models import User
from app.db import db_session


def get_all_employees(lead: User):
    """
    Вернуть всех подчинённых.
    :param lead:
    :return:
    """
    employees = db_session.query(User).filter_by(boss_id=lead.id).all()
    return employees
