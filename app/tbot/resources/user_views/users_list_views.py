from app.db import Session
from app.models import User
from app.services.dictinary import RoleService
from app.services.user import UserService
from app.tbot.services.forms.user_form import UserForm


def users_list_view(request):
    users = Session().query(User).filter(User.role != RoleService().undefined).all()
    return UserForm(models=users, page=request.page, users_list=True)


def user_view(request):
    user = UserService().by(id=request.pk())
    return UserForm(model=user, can_edit_user=True)
