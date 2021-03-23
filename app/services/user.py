from app.db import db_session
from app.models import User, Department, Role, Position
from app.services.role import get_lead


def save(user: User):
    """
    Сохранить пользователя.
    :param user:
    :return:
    """
    db_session.add(user)
    db_session.commit()


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


def is_exist(chat_id: str):
    """

    :param chat_id:
    :return:
    """
    answer = db_session.query(db_session.query(User).filter_by(chat_id=chat_id).exists()).scalar()
    return answer


def create_default(chat_id: str, username: str, fullname: str,):  # TODO Некомитеть эту функцию
    """
    Создать стандартного пользователя гостя.
    :param chat_id:
    :return:
    """
    departament = db_session.query(Department).all()[0]
    position = db_session.query(Position).all()[0]
    role = db_session.query(Role).filter_by(name='employee').first()
    user = User(chat_id=chat_id,
                username=username,
                fullname=fullname,
                department=departament,
                role=role,
                position=position,
                )
    save(user)
    return user


def is_lead(user: User):
    """
    Узнать руководитель пользователь.
    :param user:
    :return:
    """
    return user.role is get_lead()
