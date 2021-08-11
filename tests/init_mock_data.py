import json
from datetime import datetime

from loguru import logger
from sqlalchemy.exc import IntegrityError

from app.db import Session as db_session
from app.models import User, Role, Position, Department, Status, \
    ReviewPeriod, Rating, Duty, Project, Achievement, Fail, Form, HrReviewStatus, AdviceType


def commit():
    try:
        db_session.commit()
    except IntegrityError as err:
        logger.error(err)


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
    add_all_advice_types(mock_data['advice_types'])
    add_all_hr_statuses_in_db(mock_data['hr_review_statuses'])
    add_all_statuses_in_db(mock_data['statuses'])
    add_all_ratings_in_db(mock_data['ratings'])


def add_all_roles_in_db(roles_mock_data):
    """
    Добавить тестовые роли в БД.
    """
    for role_mock_data in roles_mock_data:
        if not db_session.query(db_session.query(Role).filter_by(**role_mock_data).exists()).scalar():
            role = Role(**role_mock_data)
            db_session.add(role)
            commit()


def add_all_positions_in_db(positions_mock_data):
    """
    Добавить тестовые роли в БД.
    """
    for position_mock_data in positions_mock_data:
        if not db_session.query(db_session.query(Position).filter_by(**position_mock_data).exists()).scalar():
            position = Position(**position_mock_data)
            db_session.add(position)
            commit()


def add_all_departments_in_db(departments_mock_data):
    """
    Добавить тестовые отделы в БД.
    """
    for department_mock_data in departments_mock_data:
        if not db_session.query(db_session.query(Department).filter_by(name=department_mock_data['name']).exists()).scalar():
            department = Department(name=department_mock_data['name'])
            if department_mock_data.get('positions'):
                for position in department_mock_data.get('positions'):
                    if not db_session.query(db_session.query(Position).filter_by(
                            name=position).exists()).scalar():
                        p = db_session().query(Position).filter_by(name=position).first()
                        department.positions.append(p) if p else None
            db_session.add(department)
            commit()


def add_all_users_in_db(users_mock_data):
    """
    Добавить тестовых пользователей в БД.
    """
    role = db_session.query(Role).filter_by(name='Employee').one()
    position = db_session.query(Position).filter_by(name='Разработчик').one()
    department = db_session.query(Department) \
        .filter_by(name='Разработка').one()

    for user_mock_data in users_mock_data:
        user = User(**user_mock_data)
        user.role = role
        user.position = position
        user.department = department
        logger.debug(user.role)
        db_session.add(user)
        commit()


def add_all_statuses_in_db(statuses_mock_data):
    """
    Добавить тестовые статусы в БД.
    """
    for status_mock_data in statuses_mock_data:
        if not db_session.query(db_session.query(Status).filter_by(**status_mock_data).exists()).scalar():
            status = Status(**status_mock_data)
            db_session.add(status)
            commit()


def add_all_advice_types(types_mock_data):
    """ Добавить все типы советов"""
    for advice_type in types_mock_data:
        if not db_session.query(db_session.query(AdviceType).filter_by(**advice_type).exists()).scalar():
            advice_type = AdviceType(**advice_type)
            db_session.add(advice_type)
            commit()


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
        commit()


def add_all_ratings_in_db(ratings_mock_data):
    """
    Добавить тестовые рейтинга в БД.
    """
    for rating_mock_data in ratings_mock_data:
        if not db_session.query(db_session.query(Rating).filter_by(**rating_mock_data).exists()).scalar():
            ratings = Rating(**rating_mock_data)
            db_session.add(ratings)
            commit()


def add_all_forms_in_db():
    """
    Добавить тестовые формы в БД.
    """
    users = db_session.query(User).all()
    status = db_session.query(Status).filter_by(name='Заполнение анкеты').one()
    review_period = db_session.query(ReviewPeriod).first()

    for user in users:
        form = Form()
        form.user = user
        form.status = status
        form.review_period = review_period
        db_session.add(form)
        commit()


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
        commit()


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
        commit()


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
        commit()


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
        commit()


def add_all_hr_statuses_in_db(hr_statuses_mock_data):
    for status in hr_statuses_mock_data:
        if not db_session.query(db_session.query(HrReviewStatus).filter_by(**status).exists()).scalar():
            db_session.add(HrReviewStatus(**status))
            commit()
