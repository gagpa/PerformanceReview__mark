from copy import deepcopy

from app.tbot.services.fail_service import add_wrapper

from app.models import Form
from app.services.fail_service import is_exist, get_all_text, get_all_in_form
from app.tbot.services import send_message, ask_user
from app.tbot.services.template_forms import FailsFormTemplate
from app.tbot.storages.buttons import BUTTONS


def controller_fails(message, form: Form):
    """
    :param message:
    :param form:
    :return:
    """
    buttons = []
    template = FailsFormTemplate()
    if is_exist(form=form):
        template.add(get_all_in_form(form=form))

    buttons.append([BUTTONS['fails']['add']])
    buttons.append([BUTTONS['fails']['edit_choose'], BUTTONS['fails']['delete_choose']])
    buttons.append([
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)


def controller_fails_add(message, form: Form):
    """
    Контроллер формы добавления проекта.
    :return:
    """
    template = FailsFormTemplate()

    if is_exist(form=form):
        template.add(get_all_in_form(form=form))

    next_controller = add_wrapper(controller_fails)
    ask_user(message=message,
             next_controller=next_controller,
             template=template,
             form=form,
             )


def controller_fails_edit_choose(message, form: Form):
    """

    :param message:
    :param form:
    :return:
    """
    template = FailsFormTemplate()

    fails = get_all_in_form(form)
    template.add(fails)

    buttons = [[]]
    for i, fail in enumerate(fails):
        btn = deepcopy(BUTTONS['fail']['edit'])
        btn.text = str(btn.text).format(index=i + 1)
        btn.callback_data = str(btn.callback_data).format(pk=fail.id)
        buttons[0].append(btn)
    buttons.append([
        deepcopy(BUTTONS['form']['fails']),
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)


def controller_fails_delete_choose(message, form: Form):
    """

    :param message:
    :param form:
    :return:
    """
    template = FailsFormTemplate()

    fails = get_all_in_form(form)
    template.add(fails)

    buttons = [[]]
    for i, fail in enumerate(fails):
        btn = deepcopy(BUTTONS['fail']['delete'])
        btn.text = str(btn.text).format(index=i + 1)
        btn.callback_data = str(btn.callback_data).format(pk=fail.id)
        buttons[0].append(btn)
    buttons.append([
        deepcopy(BUTTONS['form']['fails']),
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)
