from app.db import Session
from app.models import Role, Position, Department
from app.services.user import UserService
from app.tbot.resources.user_views.users_list_views import users_list_view
from app.tbot.services.auth import UserServiceTBot
from app.tbot.services.forms.user_form import UserForm


def delete_user_view(request):
    """ Удалить пользователя """
    pk = request.args['user'][0]
    service = UserService()
    user = service.by_pk(pk=pk)
    # form_service = FormService()
    # form = form_service.by(user_id=pk)
    # form_service.delete(form)
    service.delete(user)
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
        template = UserForm(changed=True)
        return template
    else:
        template = UserForm(edit_step=True)
        return template, service.add_model(change_user_fullname)


def user_edit_role(request):
    pk = request.args['user'][0]
    service = UserServiceTBot()
    user = service.by_pk(pk=pk)
    template = UserForm(models=user, edit_role_step=True)
    return template, service.add_model(change_user_role)


def change_user_role(request):
    text = request.text
    service = UserServiceTBot(model=request.model)
    if isinstance(text, str):
        service.role = Session().query(Role).filter_by(name=text).one_or_none()
        Session.add(service.model)
        Session.commit()
        template = UserForm(changed=True)
        return template
    else:
        template = UserForm(edit_step=True)
        return template, service.add_model(change_user_role)


def user_edit_position(request):
    pk = request.args['user'][0]
    service = UserServiceTBot()
    user = service.by_pk(pk=pk)
    template = UserForm(models=user, edit_position_step=True)
    return template, service.add_model(change_user_position)


def change_user_position(request):
    text = request.text
    service = UserServiceTBot(model=request.model)
    if isinstance(text, str):
        service.position = Session().query(Position).filter_by(name=text).one_or_none()
        Session.add(service.model)
        Session.commit()
        template = UserForm(changed=True)
        return template
    else:
        template = UserForm(edit_step=True)
        return template, service.add_model(change_user_role)


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
        template = UserForm(changed=True)
        return template
    else:
        template = UserForm(edit_step=True)
        return template, service.add_model(change_user_role)


def user_edit_department(request):
    pk = request.args['user'][0]
    service = UserServiceTBot()
    user = service.by_pk(pk=pk)
    template = UserForm(models=user, edit_department_step=True)
    return template, service.add_model(change_user_department)


def change_user_department(request):
    text = request.text
    service = UserServiceTBot(model=request.model)
    if isinstance(text, str):
        service.department = Session().query(Department).filter_by(name=text).one_or_none()
        Session.add(service.model)
        Session.commit()
        template = UserForm(changed=True)
        return template
    else:
        template = UserForm(edit_step=True)
        return template, service.add_model(change_user_role)
