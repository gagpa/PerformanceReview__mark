from app.db import Session
from app.models import Position, Department, Role
from app.services.user import UserService, HRService
from app.tbot import notificator
from app.tbot.services.auth import UserServiceTBot
from app.tbot.services.forms import Notification
from app.tbot.services.forms.auth_form import AuthForm


def wrong_way(request):
    user = request.user
    return AuthForm(wrong=True, user=user)


def add_new_username(request):
    """ Начать регистрацию нового пользователя """
    chat_id = request.message.chat.id
    if request.message.chat.username:
        if not UserService().is_exist(chat_id=str(chat_id)):
            positions = Session().query(Position).all()
            return AuthForm(models=positions, is_position=True)
        else:
            return AuthForm(exist=True)
    else:
        return AuthForm(no_username=True)


def add_position_user(request):
    """ Добавить должность пользователя """
    pk = request.pk()
    departments = Session().query(Department).all()
    template = AuthForm(models=departments, is_department=True, position=pk)
    return template


def add_department_user(request):
    """ Добавить отдел пользователя """
    pk = request.pk()
    position_id = request.args['position']

    service = UserServiceTBot()
    username = request.message.chat.username
    chat_id = request.message.chat.id
    user = service.create(username=username, chat_id=chat_id)

    department = Session().query(Department).get(pk)
    position = Session().query(Position).get(position_id)
    user.position = position
    user.department = department
    template = AuthForm(is_name=True)
    return template, service.add_model(add_fullname_user)


def add_fullname_user(request):
    """ Добавить ФИО пользователя """
    user = request.model
    service = UserServiceTBot(model=user)
    service.fullname = request.text
    template = AuthForm(is_boss=True, fullname=request.text)
    return template, service.add_model(add_boss_user)


def add_boss_user(request):
    """ Добавить руководителя пользователя """
    user = request.model
    service = UserServiceTBot(model=user)
    role = Session().query(Role).filter_by(name='Undefined').first()
    service.role = role
    service.boss = request.text
    user = service.model
    if HRService().all():
        notificator.notificate(Notification(view='request_for_hr', user=user),
                               *[hr.chat_id for hr in HRService().all()])
    return AuthForm(is_end=True)
