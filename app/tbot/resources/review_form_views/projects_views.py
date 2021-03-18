from copy import deepcopy

from app.models import Project, Form
from app.services.project_service import create_empty
from app.services.project_service import is_exist, get_all_in_form
from app.tbot.services import send_message, ask_user
from app.tbot.services.project_service import add_wrapper
from app.tbot.services.template_forms import ProjectsFormTemplate
from app.tbot.storages.buttons import BUTTONS


def controller_projects(message, form: Form):
    """
    Контроллер формы с проектами.
    :param message:
    :param form:
    :return:
    """
    buttons = []
    template = ProjectsFormTemplate()
    if is_exist(form=form):
        projects = get_all_in_form(form)
        template.add(projects)

    buttons.append([BUTTONS['projects']['add']])
    buttons.append([BUTTONS['project']['edit_choose'], BUTTONS['project']['delete_choose']])
    buttons.append([
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)


def controller_project_add(message, form: Form):
    """
    Контроллер формы добавления проекта.
    :param message:
    :param form:
    :return:
    """
    template = ProjectsFormTemplate()
    if is_exist(form=form):
        projects = get_all_in_form(form)
        template.add(projects)
    buttons = []
    next_controller = PROJECT_CALLBACK_LINKS[0] or add_wrapper(controller_projects)
    project = create_empty(form=form)
    ask_user(message=message,
             next_controller=next_controller,
             template=template,
             buttons=buttons,
             form=form,
             data=project
             )


def controller_add_project_name(message, form: Form, data: Project):
    """
    Контроллер для добавления названия проекта.
    :param message:
    :param form:
    :param data:
    :return:
    """
    data.name = message.text

    template = ProjectsFormTemplate()
    if is_exist(form=form):
        projects = get_all_in_form(form)
        template.add(projects)
    template.add([data])

    buttons = []
    index = PROJECT_CALLBACK_LINKS.index(controller_add_project_name)
    if PROJECT_CALLBACK_LINKS[index] != PROJECT_CALLBACK_LINKS[-1]:
        next_controller = PROJECT_CALLBACK_LINKS[index + 1]
    else:
        next_controller = add_wrapper(controller_projects)

    ask_user(message=message,
             next_controller=next_controller,
             template=template,
             buttons=buttons,
             form=form,
             data=data
             )


def controller_add_project_description(message, form: Form, data: Project):
    """
    Контроллер для добавления описания к проекту.
    :param message:
    :param form:
    :param data:
    :return:
    """
    data.description = message.text

    template = ProjectsFormTemplate()
    if is_exist(form=form):
        projects = get_all_in_form(form)
        template.add(projects)
    template.add([data])
    buttons = []
    index = PROJECT_CALLBACK_LINKS.index(controller_add_project_description)
    if PROJECT_CALLBACK_LINKS[index] != PROJECT_CALLBACK_LINKS[-1]:
        next_controller = PROJECT_CALLBACK_LINKS[index + 1]
    else:
        next_controller = add_wrapper(controller_projects)


    ask_user(message=message,
             next_controller=next_controller,
             template=template,
             buttons=buttons,
             form=form,
             data=data
             )


def controller_add_project_contacts(message, form: Form, data: Project):
    """
    Контроллер для добавления контактов проекту.
    :param message:
    :param form:
    :param data:
    :return:
    """

    # data.users = message.text
    template = ProjectsFormTemplate()
    if is_exist(form=form):
        projects = get_all_in_form(form)
        template.add(projects)
    template.add([data])

    buttons = []
    index = PROJECT_CALLBACK_LINKS.index(controller_add_project_contacts)
    if PROJECT_CALLBACK_LINKS[index] != PROJECT_CALLBACK_LINKS[-1]:
        next_controller = PROJECT_CALLBACK_LINKS[index + 1]
        ask_user(message=message,
                 next_controller=next_controller,
                 template=template,
                 buttons=buttons,
                 form=form,
                 data=data
                 )
    else:
        add_wrapper(controller_projects)(message, form, data)


from app.tbot.storages.callback_links import PROJECT_CALLBACK_LINKS
