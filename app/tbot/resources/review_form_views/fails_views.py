from app.services.achievement import is_exist, get_all_in_form
from app.services.fail import is_exist, get_all_in_form
from app.tbot.extensions import MessageManager
from app.tbot.services.achievement import add_wrapper
from app.tbot.services.fail import add_wrapper
from app.tbot.services.forms import FailsForm


def controller_fails(message):
    """ Показать провалы в форме """
    form = message.form
    fails = get_all_in_form(form) if is_exist(form=form) else None
    can_edit = bool(fails)
    template = FailsForm(fails, can_add=True, can_edit=can_edit, can_del=can_edit)
    MessageManager.send_message(message=message, template=template)


def controller_fails_add(message):
    """ Добавить один или несколько провалов """
    form = message.form
    fails = get_all_in_form(form) if is_exist(form=form) else None
    template = FailsForm(fails, can_add=False, can_del=False, can_edit=False)

    next_controller = add_wrapper(controller_fails)
    MessageManager.ask_user(message=message, template=template, next_controller=next_controller)


def controller_fails_edit_choose(message):
    """ Выбрать провал для изменения """
    form = message.form
    fails = get_all_in_form(form) if is_exist(form=form) else None
    template = FailsForm(fails, can_add=False, can_edit=True, can_del=False)
    MessageManager.send_message(message=message, template=template)


def controller_fails_delete_choose(message):
    """ Выбрать провал для удаления """
    form = message.form
    fails = get_all_in_form(form) if is_exist(form=form) else None
    template = FailsForm(fails, can_add=False, can_edit=False, can_del=True)
    MessageManager.send_message(message=message, template=template)


__all__ = \
    [
        'controller_fails',
        'controller_fails_add',
        'controller_fails_edit_choose',
        'controller_fails_delete_choose'
    ]
