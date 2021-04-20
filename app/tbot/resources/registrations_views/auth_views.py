from app.db import Session
from app.models import Position, Department, Role
from app.services.user import UserService
from app.tbot.services.auth import UserServiceTBot
from app.tbot.services.forms.auth_form import AuthForm


def add_new_username(request):
    """ Начать регистрацию нового пользователя """
    service = UserServiceTBot()
    username = request.message.chat.username
    chat_id = request.message.chat.id
    if not UserService().is_exist(chat_id=str(chat_id)):
        user = service.create(username=username, chat_id=chat_id)
        template = AuthForm(is_name=True)
        return template, service.add_model(add_fullname_user)
    else:
        return AuthForm(exist=True)


def add_fullname_user(request):
    """ Добавить должность пользователя """
    user = request.model
    text = request.text
    service = UserServiceTBot(model=user)
    if isinstance(text, str):
        service.fullname = text
        template = AuthForm(is_position=True)
        return template, service.add_model(add_position_user)
    else:
        template = AuthForm(is_not_name=True)
        return template, service.add_model(add_fullname_user)


def add_position_user(request):
    """ Добавить должность пользователя """
    user = request.model
    text = request.text
    service = UserServiceTBot(model=user)
    position = Session().query(Position).filter_by(name=text).one_or_none()
    if position:
        service.position = position
        template = AuthForm(is_department=True)
        return template, service.add_model(add_department_user)
    else:
        template = AuthForm(is_not_position=True)
        return template, service.add_model(add_position_user)


def add_department_user(request):
    """ Добавить отдел пользователя """
    user = request.model
    text = request.text
    service = UserServiceTBot(model=user)
    department = Session().query(Department).filter_by(name=text).one_or_none()
    if department:
        service.department = department
        template = AuthForm(is_boss=True)
        return template, service.add_model(add_boss_user)
    else:
        template = AuthForm(is_not_department=True)
        return template, service.add_model(add_department_user)


def add_boss_user(request):
    """ Добавить руководителя пользователя """
    user = request.model
    service = UserServiceTBot(model=user)
    role = Session().query(Role).filter_by(name='Undefined').first()
    service.role = role
    service.boss = request.text
    template = AuthForm(is_end=True)
    return template
