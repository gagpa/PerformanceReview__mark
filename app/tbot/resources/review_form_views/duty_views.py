"""
View обязанности.
"""
from app.models import Form
from app.services.duty_service import is_exist, get
from app.tbot.services.duty_service import add_wrapper, edit_wrapper
from app.tbot.services.template_forms import DutyFormTemplate
from app.tbot.storages.buttons import BUTTONS
from app.tbot.services import send_message, ask_user


def controller_duty(message, form: Form):
    """
    Контроллер формы заполнения обязанностей.
    :param message:
    :param form:
    :return:
    """
    buttons = []
    template = DutyFormTemplate()
    if is_exist(form):
        duty = get(form=form)
        template.add(duty)
        buttons.append([BUTTONS['duty']['edit']])
        buttons.append([BUTTONS['default']['form']])
    else:
        buttons.append([BUTTONS['duty']['add']])
        buttons.append([BUTTONS['default']['form']])
    send_message(message=message, template=template, buttons=buttons)


def controller_duty_add(message, form: Form):
    """
    Контроллер формы добавления обязанностей.
    :param message:
    :param form:
    :return:
    """

    buttons = None

    template = DutyFormTemplate()
    ask_user(message=message,
             next_controller=add_wrapper(controller_duty),
             template=template,
             buttons=buttons,
             form=form)


def controller_duty_edit(message, form: Form):
    """
    Изменить обязанности пользователя.
    :param message:
    :param form:
    :return:
    """
    buttons = None

    template = DutyFormTemplate()
    duty = get(form=form)
    template.add(duty)
    ask_user(message=message,
             next_controller=edit_wrapper(controller_duty),
             template=template,
             buttons=buttons,
             form=form)
