"""
View обязанности.
"""
from app.services.duty import is_exist, get
from app.tbot.extensions import MessageManager
from app.tbot.services.duty import add_wrapper, edit_wrapper
from app.tbot.services.forms import DutyForm


def controller_duty(message):
    """  Показать обязанность в форме """
    form = message.form
    duty = get(form=form) if is_exist(form) else None
    can_edit = bool(duty)
    template = DutyForm(duty, can_add=not can_edit, can_edit=can_edit)
    MessageManager.send_message(message=message, template=template)


def controller_duty_add(message):
    """ Добавить обязанность """
    template = DutyForm(can_add=False, can_edit=False)
    MessageManager.ask_user(message=message, template=template, next_controller=add_wrapper(controller_duty))


def controller_duty_edit(message):
    """ Изменить обязанность """
    form = message.form
    duty = get(form=form)
    template = DutyForm(duty, can_add=False, can_edit=False)
    MessageManager.ask_user(message=message, template=template, next_controller=edit_wrapper(controller_duty))


__all__ = \
    [
        'controller_duty',
        'controller_duty_add',
        'controller_duty_edit',
    ]
