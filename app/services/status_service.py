from app.models import Status
from app.db import db_session


def get_for_new_form():
    """
    Вернуть статус для новой формы.
    :return:
    """
    status = db_session.query(Status).filter_by(name='Заполнение анкеты').first()
    return status
