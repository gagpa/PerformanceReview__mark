from app.db import Session
from app.models import Role, Position, Department
from app.services.user import UserService
from app.tbot import notificator
from app.tbot.resources.user_views.users_list_views import users_list_view
from app.tbot.services.auth import UserServiceTBot
from app.tbot.services.forms.notification import Notification
from app.tbot.services.forms.user_form import UserForm


def delete_user_view(request):
    """ Подтвердить удаление """
    pk = request.args['user'][0]
    service = UserService()
    user = service.by_pk(pk=pk)
    return UserForm(confirm=True, user=True, model=user)


def delete_user(request):
    """ Удалить пользователя """
    pk = request.args['user'][0]
    service = UserServiceTBot()
    user = service.by_pk(pk=pk)
    user.boss = None
    for form in user.forms:
        for project in form.projects:
            if project.reviews:
                service.delete(project.reviews)
    service.delete(user)
    notificator.notificate(Notification(view='delete_user'), user.chat_id)
    request.add('dep', [user.department.id])
    return users_list_view(request=request)


def edit_user_view(request):
    """ Изменить данные пользователя """
    pk = request.args['user'][0]
    service = UserServiceTBot()
    user = service.by_pk(pk=pk)
    return UserForm(model=user, edit_step=True)


def user_edit_fullname(request):
    pk = request.args['user'][0]
    service = UserServiceTBot()
    user = service.by_pk(pk=pk)
    template = UserForm(models=user, edit_fullname_step=True)
    return template, service.add_model(change_user_fullname)


def change_user_fullname(request):
    text = request.text
    service = UserServiceTBot(model=request.model)
    if isinstance(text, str):
        service.fullname = text
        Session.add(service.model)
        Session.commit()
        return UserForm(model=service.model, can_edit_user=True)
    else:
        template = UserForm(edit_step=True)
        return template, service.add_model(change_user_fullname)


def user_edit_role(request):
    pk = request.args['user'][0]
    roles = Session().query(Role).filter(Role.name != 'Undefined').all()
    template = UserForm(user_id=pk, roles=roles, edit_role_step=True)
    return template


def change_user_role(request):
    pk = request.pk()
    user_id = request.args['user_id'][0]
    user = UserServiceTBot().by_pk(user_id)
    user.role = Session().query(Role).get(pk)
    Session.add(user)
    Session.commit()
    chat_id = user.chat_id
    notificator.notificate(Notification(view='change_role', role=user.role.name), chat_id)
    return UserForm(model=user, can_edit_user=True)


def user_edit_position(request):
    pk = request.args['user'][0]
    user = UserServiceTBot().by_pk(pk)
    positions = user.department.positions
    return UserForm(user_id=pk, positions=positions, edit_position_step=True)


def change_user_position(request):
    pk = request.pk()
    user_id = request.args['user_id'][0]
    user = UserServiceTBot().by_pk(user_id)
    user.position = Session().query(Position).get(pk)
    Session.add(user)
    Session.commit()
    return UserForm(model=user, can_edit_user=True)


def user_edit_boss(request):
    pk = request.args['user'][0]
    service = UserServiceTBot()
    user = service.by_pk(pk=pk)
    template = UserForm(models=user, edit_boss_step=True)
    return template, service.add_model(change_user_boss)


def change_user_boss(request):
    text = request.text
    service = UserServiceTBot(model=request.model)
    if isinstance(text, str):
        service.boss = text
        Session.add(service.model)
        Session.commit()
        return UserForm(model=service.model, can_edit_user=True)
    else:
        template = UserForm(edit_step=True)
        return template, service.add_model(change_user_role)


def user_edit_department(request):
    pk = request.args['user'][0]
    departments = Session().query(Department).all()
    return UserForm(user_id=pk, departments=departments, edit_department_step=True)


def change_user_department(request):
    pk = request.pk()
    user_id = request.args['user_id'][0]
    user = UserServiceTBot().by_pk(user_id)
    user.department = Session().query(Department).get(pk)
    Session.add(user)
    Session.commit()
    return UserForm(model=user, can_edit_user=True)
