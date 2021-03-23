from app.db import db_session
from app.models import Achievement, Form


def save(achievement: Achievement):
    db_session.add(achievement)
    db_session.commit()


def create_empty(form: Form):
    """

    :param form:
    :return:
    """
    return Achievement(form=form)


def delete(achievement: Achievement):
    """
    Создать достижение за текущее review.
    """
    db_session.delete(achievement)
    db_session.commit()


def is_exist(form) -> bool:
    """
    Проверить существование достижения.
    :param form:
    :return:
    """
    answer = db_session.query(db_session.query(Achievement).filter(Achievement.form == form).exists()).scalar()
    return answer


def get_all_text(form) -> list:
    """
    Вернуть достижения пользователя.
    :param form:
    :return:
    """
    achievements = get_all_in_form(form=form)
    achievements = [achievement.text for achievement in achievements]
    return achievements


def get_all_in_form(form) -> list:
    achievements = db_session.query(Achievement).filter_by(form=form).all()
    return achievements


def get_for_pk(pk: int) -> Achievement:
    """

    :param pk:
    :return:
    """
    achievement = db_session.query(Achievement).filter_by(id=pk).first()
    return achievement
