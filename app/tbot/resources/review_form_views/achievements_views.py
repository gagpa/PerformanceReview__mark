from app.services.achievement import is_exist, get_all_in_form
from app.tbot.extensions import MessageManager
from app.tbot.services.achievement import add_wrapper
from app.tbot.services.forms import AchievementsForm


def controller_achievements(message):
    """ Показать все достижения в форме """
    form = message.form
    achievements = get_all_in_form(form) if is_exist(form=form) else None
    can_edit = bool(achievements)
    template = AchievementsForm(achievements, can_add=True, can_edit=can_edit, can_del=can_edit)
    MessageManager.send_message(message=message, template=template)


def controller_achievements_add(message):
    """ Добавить одно или несколько достижений в форму """
    form = message.form
    achievements = get_all_in_form(form) if is_exist(form=form) else None
    template = AchievementsForm(achievements, can_add=False, can_del=False, can_edit=False)

    next_controller = add_wrapper(controller_achievements)
    MessageManager.ask_user(message=message, template=template, next_controller=next_controller)


def controller_achievements_edit_choose(message):
    """ Выбрать достижение для изменения """
    form = message.form
    achievements = get_all_in_form(form) if is_exist(form=form) else None
    template = AchievementsForm(achievements, can_add=False, can_edit=True, can_del=False)
    MessageManager.send_message(message=message, template=template)


def controller_achievements_delete_choose(message):
    """ Выбрать достижение для удаления """
    form = message.form
    achievements = get_all_in_form(form) if is_exist(form=form) else None
    template = AchievementsForm(achievements, can_add=False, can_edit=False, can_del=True)
    MessageManager.send_message(message=message, template=template)


__all__ = \
    [
        'controller_achievements',
        'controller_achievements_add',
        'controller_achievements_edit_choose',
        'controller_achievements_delete_choose',
    ]
