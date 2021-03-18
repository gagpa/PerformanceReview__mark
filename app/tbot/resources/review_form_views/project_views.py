from copy import deepcopy

from app.models import Form
from app.services.project_service import get_all_in_form, delete, get_for_pk
from app.tbot.resources.review_form_views.projects_views import controller_projects
from app.tbot.services.message_service import send_message, ask_user
from app.tbot.services.project_service import edit_name_wrapper, edit_contacts_wrapper, edit_description_wrapper
from app.tbot.services.template_forms import ProjectsFormTemplate, ProjectFormTemplate
from app.tbot.storages.buttons import BUTTONS


def controller_project_edit_choose(message, form: Form):
    """
    Контроллер для выбора изменения проекта.
    :param message:
    :param form:
    :return:
    """
    template = ProjectsFormTemplate()
    projects = get_all_in_form(form)
    template.add(projects)

    buttons = [[]]
    for i, project in enumerate(projects):
        btn = deepcopy(BUTTONS['project']['edit'])
        btn.text = str(btn.text).format(index=i + 1)
        btn.callback_data = str(btn.callback_data).format(pk=project.id)
        buttons[0].append(btn)
    buttons.append([
        deepcopy(BUTTONS['form']['projects']),
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)


def controller_project_edit(call, form):
    """

    :param message:
    :param form:
    :return:
    """
    buttons = []

    pk = int(call.data.split(' ')[-1])

    project = get_for_pk(pk)
    template = ProjectFormTemplate()
    template.add(project)
    buttons.append([
        deepcopy(BUTTONS['project']['name']),
        deepcopy(BUTTONS['project']['description']),
        deepcopy(BUTTONS['project']['contacts']),
    ])
    buttons.append([
        deepcopy(BUTTONS['form']['projects']),
        deepcopy(BUTTONS['default']['form']),
    ])

    for btn in buttons[0]:
        btn.callback_data = str(btn.callback_data).format(pk=project.id)

    send_message(message=call.message, template=template, buttons=buttons)


def controller_project_edit_name(call, form):
    """

    :param message:
    :param form:
    :return:
    """
    pk = int(call.data.split(' ')[-1])

    project = get_for_pk(pk)
    template = ProjectsFormTemplate()

    ask_user(message=call.message,
             next_controller=edit_name_wrapper(controller_project_edit),
             template=template,
             form=form,
             data=project
             )


def controller_project_edit_contacts(call, form):
    """

    :param message:
    :param form:
    :return:
    """
    pk = int(call.data.split(' ')[-1])

    project = get_for_pk(pk)
    template = ProjectsFormTemplate()

    ask_user(message=call.message,
             next_controller=edit_contacts_wrapper(controller_project_edit),
             template=template,
             form=form,
             data=project
             )


def controller_project_edit_description(call, form):
    """

    :param message:
    :param form:
    :return:
    """
    pk = int(call.data.split(' ')[-1])

    project = get_for_pk(pk)
    template = ProjectsFormTemplate()

    ask_user(message=call.message,
             next_controller=edit_description_wrapper(controller_project_edit),
             template=template,
             form=form,
             data=project
             )


def controller_project_delete_choose(message, form: Form):
    """
    Контроллер для удаления проекта.
    :param message:
    :param form:
    :return:
    """
    template = ProjectsFormTemplate()
    projects = get_all_in_form(form)
    # template.add_projects()

    buttons = [[]]
    for i, project in enumerate(projects):
        btn = deepcopy(BUTTONS['project']['delete'])
        btn.text = str(btn.text).format(index=i + 1)
        btn.callback_data = str(btn.callback_data).format(pk=project.id)
        buttons[0].append(btn)
    buttons.append([
        deepcopy(BUTTONS['form']['projects']),
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)


def controller_project_delete(call, form):
    """

    :param message:
    :param form:
    :return:
    """
    pk = int(call.data.split(' ')[-1])

    project = get_for_pk(pk)
    delete(project)

    controller_projects(message=call.message, form=form)
