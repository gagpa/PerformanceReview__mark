from app.db import Session
from app.models import User, Department
from app.services.dictinary import RoleService
from app.services.user import UserService
from app.tbot.services.forms.user_form import UserForm


def choose_departments_view(request):
    departments = Session().query(Department).all()
    return UserForm(models=departments, choose_dep=True)


def users_list_view(request):
    dep_id = request.args['dep'][0]
    department = Session().query(Department).filter_by(id=dep_id).first()
    users = Session().query(User).filter(User.role != RoleService().undefined, User.department == department).order_by(User.position_id).all()
    return UserForm(models=users, page=request.page, users_list=True, department=department)


def user_view(request):
    user = UserService().by(id=request.pk())
    return UserForm(model=user, can_edit_user=True)
