from app.tbot.services import ProjectsServiceTBot
from app.tbot.services.forms import ProjectsForm


def list_view(request):
    """ Показать все проекте в анкете """
    form = request.form
    service = ProjectsServiceTBot(form=form)
    projects = service.all
    return ProjectsForm(projects=projects, review_type='write', view='list', have_markup=True)


def edit_choose_view(request):
    """ Выбрать проект для изменения """
    form = request.form
    service = ProjectsServiceTBot(form=form)
    projects = service.all
    template = ProjectsForm(projects=projects, review_type='write', view='edit_choose', have_markup=True)
    return template


def delete_choose_view(request):
    """ Выбрать проект для удаления """
    form = request.form
    service = ProjectsServiceTBot(form=form)
    projects = service.all
    template = ProjectsForm(projects=projects, review_type='write', view='delete_choose', have_markup=True)
    return template


__all__ = \
    [
        'list_view',
        'edit_choose_view',
        'delete_choose_view',
    ]
