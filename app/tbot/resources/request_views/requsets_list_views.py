from app.services.dictinary import RoleService
from app.services.user import UserService
from app.tbot.services.forms.user_form import UserForm


def request_list_view(request):
    requests = UserService().all_by(role=RoleService().undefined)
    return UserForm(models=requests, page=request.page, requests=True)


def request_view(request):
    request = UserService().by(id=request.pk())
    return UserForm(model=request, can_edit=True)
