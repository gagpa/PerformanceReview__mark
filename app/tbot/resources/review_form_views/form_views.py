from app.models import Form
from app.tbot.services import send_message
from app.tbot.services.template_forms import FormTemplate
from app.tbot.storages.buttons import BUTTONS


def controller_form(message, form: Form):
    """
    Контроллер формы анкеты.
    :return:
    """
    buttons = []

    template = FormTemplate()
    if form:
        template.add(form)

    buttons.append([BUTTONS['form']['duty'], BUTTONS['form']['projects']])
    buttons.append([BUTTONS['form']['achievements'], BUTTONS['form']['fails']])
    send_message(message=message, template=template, buttons=buttons)
