from app.tbot.services import AchievementServiceTBot
from app.tbot.services.forms import AchievementsForm


def list_view(request):
    """ Показать все достижения в форме """
    form = request.form
    achievement_service = AchievementServiceTBot(form=form)
    achievements = achievement_service.all
    can_edit = bool(achievements)
    template = AchievementsForm(models=achievements, can_add=True, can_edit=can_edit, can_del=can_edit)
    return template


def add_view(request):
    """ Добавить одно или несколько достижений в форму """
    form = request.form
    achievement_service = AchievementServiceTBot(form=form)
    achievements = achievement_service.all
    template = AchievementsForm(models=achievements, can_add=False, can_del=False, can_edit=False)
    next_view = achievement_service.create_before(list_view)
    return template, next_view


def edit_choose_view(request):
    """ Выбрать достижение для изменения """
    form = request.form
    achievement_service = AchievementServiceTBot(form=form)
    achievements = achievement_service.all
    template = AchievementsForm(models=achievements, can_add=False, can_edit=True, can_del=False)
    return template


def delete_choose_view(request):
    """ Выбрать достижение для удаления """
    form = request.form
    achievement_service = AchievementServiceTBot(form=form)
    achievements = achievement_service.all
    template = AchievementsForm(models=achievements, can_add=False, can_edit=False, can_del=True)
    return template


__all__ = \
    [
        'list_view',
        'add_view',
        'edit_choose_view',
        'delete_choose_view',
    ]
