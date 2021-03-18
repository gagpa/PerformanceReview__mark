from copy import deepcopy

from app.tbot.services.achievement_service import add_wrapper

from app.models import Form
from app.services.achievement_service import is_exist, get_all_text, get_all_in_form
from app.tbot.services import send_message, ask_user
from app.tbot.services.template_forms import AchievementsFormTemplate
from app.tbot.storages.buttons import BUTTONS


def controller_achievements(message, form: Form):
    """
    :param message:
    :param form:
    :return:
    """
    buttons = []
    template = AchievementsFormTemplate()
    if is_exist(form=form):
        template.add(get_all_in_form(form=form))

    buttons.append([BUTTONS['achievements']['add']])
    buttons.append([BUTTONS['achievements']['edit_choose'], BUTTONS['achievements']['delete_choose']])
    buttons.append([
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)


def controller_achievements_add(message, form: Form):
    """
    Контроллер формы добавления проекта.
    :return:
    """
    template = AchievementsFormTemplate()
    if is_exist(form=form):
        template.add(get_all_in_form(form=form))

    next_controller = add_wrapper(controller_achievements)
    ask_user(message=message,
             next_controller=next_controller,
             template=template,
             form=form,
             )


def controller_achievements_edit_choose(message, form: Form):
    """

    :param message:
    :param form:
    :return:
    """
    template = AchievementsFormTemplate()

    achievements = get_all_in_form(form)
    template.add(achievements)

    buttons = [[]]
    for i, achievement in enumerate(achievements):
        btn = deepcopy(BUTTONS['achievement']['edit'])
        btn.text = str(btn.text).format(index=i + 1)
        btn.callback_data = str(btn.callback_data).format(pk=achievement.id)
        buttons[0].append(btn)
    buttons.append([
        deepcopy(BUTTONS['form']['achievements']),
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)


def controller_achievements_delete_choose(message, form: Form):
    """

    :param message:
    :param form:
    :return:
    """
    template = AchievementsFormTemplate()

    achievements = get_all_in_form(form)
    template.add(achievements)

    buttons = [[]]
    for i, achievement in enumerate(achievements):
        btn = deepcopy(BUTTONS['achievement']['delete'])
        btn.text = str(btn.text).format(index=i + 1)
        btn.callback_data = str(btn.callback_data).format(pk=achievement.id)
        buttons[0].append(btn)
    buttons.append([
        deepcopy(BUTTONS['form']['achievements']),
        deepcopy(BUTTONS['default']['form']),
    ])
    send_message(message=message, template=template, buttons=buttons)
