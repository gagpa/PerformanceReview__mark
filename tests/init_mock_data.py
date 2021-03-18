import json
from datetime import datetime

from loguru import logger

from app.db import db_session
from app.models import User, Role, Position, Department, Status,\
    ReviewPeriod, Rating, Duty, Project, Achievement, Fail, Form


def get_mock_data() -> dict:
    """
    Получить тестовые данные.
    Открывает файл mock_data.json и формирует словарь(dict).
    """
    with open('tests/mock_data.json') as file:
        mock_data = json.load(file)
        return mock_data


def add_all_mock_data_in_db():
    """
    Добавить тестовые данные в БД.
    """
    mock_data = get_mock_data()

    add_all_roles_in_db(mock_data['roles'])
    add_all_positions_in_db(mock_data['positions'])
    add_all_departments_in_db(mock_data['departments'])
    add_all_users_in_db(mock_data['users'])

    add_all_statuses_in_db(mock_data['statuses'])
    add_all_review_periods_in_db(mock_data['review_periods'])
    add_all_ratings_in_db(mock_data['ratings'])

    add_all_forms_in_db()

    add_all_duties_in_db(mock_data['duties'])
    add_all_projects_in_db(mock_data['projects'])
    add_all_achievements_in_db(mock_data['achievements'])
    add_all_fails_in_db(mock_data['fails'])


def add_all_roles_in_db(roles_mock_data):
    """
    Добавить тестовые роли в БД.
    """
    for role_mock_data in roles_mock_data:
        role = Role(**role_mock_data)
        db_session.add(role)

    db_session.commit()


def add_all_positions_in_db(positions_mock_data):
    """
    Добавить тестовые роли в БД.
    """
    for position_mock_data in positions_mock_data:
        position = Position(**position_mock_data)
        db_session.add(position)

    db_session.commit()


def add_all_departments_in_db(departments_mock_data):
    """
    Добавить тестовые отделы в БД.
    """
    for department_mock_data in departments_mock_data:
        department = Department(**department_mock_data)
        db_session.add(department)

    db_session.commit()


def add_all_users_in_db(users_mock_data):
    """
    Добавить тестовых пользователей в БД.
    """
    role = db_session.query(Role).filter_by(name='Employee').one()
    position = db_session.query(Position).filter_by(name='Главный специалист').one()
    department = db_session.query(Department).filter_by(name='разработчики').one()

    for user_mock_data in users_mock_data:
        user = User(**user_mock_data)
        user.role = role
        user.position = position
        user.department = department
        logger.debug(user.role)
        db_session.add(user)

    db_session.commit()


def add_all_statuses_in_db(statuses_mock_data):
    """
    Добавить тестовые статусы в БД.
    """
    for status_mock_data in statuses_mock_data:
        status = Status(**status_mock_data)
        db_session.add(status)

    db_session.commit()


def add_all_review_periods_in_db(review_periods_mock_data):
    """
    Добавить тестовые периоды review в БД.
    """
    for review_period_mock_data in review_periods_mock_data:
        review_period = ReviewPeriod()
        review_period.is_active = review_period_mock_data['is_active']
        review_period.start_date = datetime.now()
        review_period.end_date = datetime.now()
        db_session.add(review_period)

    db_session.commit()


def add_all_ratings_in_db(ratings_mock_data):
    """
    Добавить тестовые рейтинга в БД.
    """
    for rating_mock_data in ratings_mock_data:
        ratings = Rating(**rating_mock_data)
        db_session.add(ratings)

    db_session.commit()


def add_all_forms_in_db():
    """
    Добавить тестовые формы в БД.
    """
    users = db_session.query(User).all()
    status = db_session.query(Status).filter_by(name='Заполнение анкеты').one()
    review_period = db_session.query(ReviewPeriod).first()
    rating = db_session.query(Rating).filter_by(value=3).one()

    for user in users:
        form = Form()
        form.user = user
        form.status = status
        form.review_period = review_period
        form.rating = rating
        db_session.add(form)

    db_session.commit()


def add_all_duties_in_db(duties_mock_data):
    """
    Добавить тестовые обязанностей в БД.
    """
    forms = db_session.query(Form).all()
    for i, form in enumerate(forms):
        if i < len(duties_mock_data):
            duty = Duty(**duties_mock_data[i])
            duty.form = form
            db_session.add(duty)

    db_session.commit()


def add_all_projects_in_db(projects_mock_data):
    """
    Добавить тестовые проекты в БД.
    """
    forms = db_session.query(Form).all()
    for i, form in enumerate(forms):
        if i < len(projects_mock_data):
            project = Project(**projects_mock_data[i])
            project.form = form
            db_session.add(project)

    db_session.commit()


def add_all_achievements_in_db(achievements_mock_data):
    """
    Добавить тестовые обязанностей в БД.
    """
    forms = db_session.query(Form).all()
    for i, form in enumerate(forms):
        if i < len(achievements_mock_data):
            achievement = Achievement(**achievements_mock_data[i])
            achievement.form = form
            db_session.add(achievement)

    db_session.commit()


def add_all_fails_in_db(fails_mock_data):
    """
    Добавить тестовые провалы в БД.
    """
    forms = db_session.query(Form).all()
    for i, form in enumerate(forms):
        if i < len(fails_mock_data):
            fail = Fail(**fails_mock_data[i])
            fail.form = form
            db_session.add(fail)

    db_session.commit()
