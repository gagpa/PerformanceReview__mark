from app.db import Session
from app.models import Role
from app.services.form_review import FormService
from app.services.user import UserService
from app.tbot import notificator
from app.tbot.resources.request_views import request_list_view
from app.tbot.services.auth import UserServiceTBot
from app.tbot.services.forms import Notification
from app.tbot.services.forms.user_form import UserForm


def delete_request_view(request):
    """ Подтвердить удаление """
    pk = request.args['user'][0]
    service = UserService()
    user = service.by_pk(pk=pk)
    return UserForm(confirm=True, request=True, model=user)


def delete_request(request):
    """ Удалить запрос """
    pk = request.args['user'][0]
    service = UserService()
    user = service.by_pk(pk=pk)
    form_service = FormService()
    form = form_service.by(user_id=pk)
    if form:
        form_service.delete(form)
    notificator.notificate(Notification(view='delete_user'), user.chat_id)
    service.delete(user)
    return request_list_view(request=request)


def accept_request_view(request):
    """ Добавить пользователя """
    pk = request.args['user'][0]
    service = UserServiceTBot()
    user = service.by_pk(pk=pk)
    user.role = Session().query(Role).filter_by(name='Employee').one_or_none()
    sess = Session().object_session(user)
    sess.commit()
    chat_id = user.chat_id
    notificator.notificate(Notification(view='add_role', role=user.role.name), chat_id)
    return request_list_view(request=request)
