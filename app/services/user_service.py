from app.db import db_session
from app.models import User


def get(chat_id: str) -> User:
    """
    Выдать id пользователя.
    :return:
    """
    user = db_session.query(User).filter_by(chat_id=str(chat_id)).first()
    return user


def get_for_username(username: str) -> User:
    user = db_session.query(User).filter_by(username=username).first()
    return user
