from app.services.project import is_exist, get_all_in_form
from app.tbot.extensions import MessageManager
from app.tbot.services.forms import ProjectsForm


def controller_projects(message):
    """ Показать все проекте в анкете """
    form = message.form
    projects = get_all_in_form(form) if is_exist(form=form) else None
    can_edit = bool(projects)
    template = ProjectsForm(projects, can_add=True, can_edit=can_edit, can_del=can_edit)
    MessageManager.send_message(message=message, template=template)


def controller_project_edit_choose(message):
    """ Выбрать проект для изменения """
    form = message.form
    projects = get_all_in_form(form)
    template = ProjectsForm(projects, can_edit=True)
    MessageManager.send_message(message=message, template=template)


def controller_project_delete_choose(message):
    """ Выбрать проект для удаления """
    form = message.form
    projects = get_all_in_form(form)
    template = ProjectsForm(projects, can_del=True)
    MessageManager.send_message(message=message, template=template)


__all__ = \
    [
        'controller_projects',
        'controller_project_edit_choose',
        'controller_project_delete_choose',
    ]
