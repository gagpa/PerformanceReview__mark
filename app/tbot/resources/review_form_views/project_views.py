from app.services.project import create_empty
from app.services.project import delete, get_for_pk
from app.tbot.extensions import MessageManager
from app.tbot.resources.review_form_views.projects_views import controller_projects
from app.tbot.services.forms import ProjectForm
from app.tbot.services.project import add_wrapper
from app.tbot.services.project import edit_name_wrapper, edit_contacts_wrapper, edit_description_wrapper


def controller_project_edit(message):
    """ Изменить проект """
    pk = message.pk
    project = get_for_pk(pk)
    template = ProjectForm(project, can_edit=True)
    MessageManager.send_message(message=message, template=template)


def controller_project_edit_name(message):
    """ Изменить имя проекта """
    pk = message.pk
    project = get_for_pk(pk)
    template = ProjectForm(project, can_add=True, is_name=True)
    message.model = project
    MessageManager.ask_user(message=message, template=template,
                            next_controller=edit_name_wrapper(controller_project_edit))


def controller_project_edit_contacts(message):
    """ Изменить контакты к проекту """
    pk = message.pk
    project = get_for_pk(pk)
    template = ProjectForm(project, can_add=True, is_contacts=True)
    message.model = project
    MessageManager.ask_user(message=message, template=template,
                            next_controller=edit_contacts_wrapper(controller_project_edit))


def controller_project_edit_description(message):
    """ Измнить описание проекта """
    pk = message.pk
    project = get_for_pk(pk)
    template = ProjectForm(project, can_add=True, is_description=True)
    message.model = project
    MessageManager.ask_user(message=message, template=template,
                            next_controller=edit_description_wrapper(controller_project_edit))


def controller_project_delete(message):
    """ Удалить проект """
    pk = message.pk
    project = get_for_pk(pk)
    delete(project)
    controller_projects(message=message)


def controller_project_add(message):
    """ Добавить новый проект """
    form = message.form
    message.model = create_empty(form)
    template = ProjectForm(message.model, can_add=True, is_name=True)
    MessageManager.ask_user(message=message, template=template, next_controller=controller_add_project_name)


def controller_add_project_name(message, model):
    """ Добавить название проекта """
    model.name = message.text
    message.model = model
    template = ProjectForm(model, can_add=True, is_description=True)
    next_controller = controller_add_project_description
    MessageManager.ask_user(message=message, template=template, next_controller=next_controller)


def controller_add_project_description(message, model):
    """ Добавить описание проекта """
    model.description = message.text
    message.model = model
    template = ProjectForm(model, can_add=True, is_contacts=True)
    next_controller = controller_add_project_contacts
    MessageManager.ask_user(message=message, template=template, next_controller=next_controller)


def controller_add_project_contacts(message, model):
    """ Добавить контакты проекта """
    # message.data.users = message.text
    message.model = model
    add_wrapper(controller_projects)(message)


__all__ = \
    [
        'controller_project_edit',
        'controller_project_edit_name',
        'controller_project_edit_contacts',
        'controller_project_edit_description',
        'controller_project_delete',
        'controller_project_add',
        'controller_add_project_name',
        'controller_add_project_description',
        'controller_add_project_contacts',
    ]
