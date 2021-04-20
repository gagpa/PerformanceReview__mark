from app.tbot.services import ProjectsServiceTBot
from app.tbot.services.forms import ProjectsForm


def list_view(request):
    """ Показать все проекте в анкете """
    form = request.form
    service = ProjectsServiceTBot(form=form)
    projects = service.all
    can_edit = bool(projects)
    template = ProjectsForm(models=projects, can_add=True, can_edit=can_edit, can_del=can_edit)
    return template


def edit_choose_view(request):
    """ Выбрать проект для изменения """
    form = request.form
    service = ProjectsServiceTBot(form=form)
    projects = service.all
    template = ProjectsForm(models=projects, can_edit=True)
    return template


def delete_choose_view(request):
    """ Выбрать проект для удаления """
    form = request.form
    service = ProjectsServiceTBot(form=form)
    projects = service.all
    template = ProjectsForm(models=projects, can_del=True)
    return template


__all__ = \
    [
        'list_view',
        'edit_choose_view',
        'delete_choose_view',
    ]
