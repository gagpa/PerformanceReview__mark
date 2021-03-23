from app.db import db_session
from app.models import Project, Form


def save(project: Project):
    """
    Создать проект за текущее review.
    """
    db_session.add(project)
    db_session.commit()


def create_empty(form: Form) -> Project:
    """
    Создать пустой проект.
    """
    project = Project(form=form)
    return project


def is_exist(form: Form) -> bool:
    """
    Проверить существование проектов.
    :param form:
    :return:
    """
    answer = db_session.query(db_session.query(Project).filter(Project.form == form).exists()).scalar()
    return answer


def delete(project: Project):
    db_session.delete(project)
    db_session.commit()


def get_all_in_form(form: Form):
    """
    Вернуть все проекты из формы.
    :param form:
    :return:
    """
    projects = db_session.query(Project).filter_by(form=form).all()
    return projects


def get_for_pk(pk: int):
    """
    Получить проект по pk.
    :param pk:
    :return:
    """
    project = db_session.query(Project).filter_by(id=pk).first()
    return project
