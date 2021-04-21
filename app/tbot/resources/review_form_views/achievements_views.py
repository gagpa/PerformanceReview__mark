from app.tbot.services import AchievementServiceTBot
from app.tbot.services.forms import AchievementsForm


def list_view(request):
    """ Показать все достижения в форме """
    form = request.form
    achievement_service = AchievementServiceTBot(form=form)
    achievements = achievement_service.all
    template = AchievementsForm(achievements=achievements, view='list')
    return template


def add_view(request):
    """ Добавить одно или несколько достижений в форму """
    form = request.form
    achievement_service = AchievementServiceTBot(form=form)
    achievements = achievement_service.all
    template = AchievementsForm(achievements=achievements, view='add')
    next_view = achievement_service.create_before(list_view)
    return template, next_view


def edit_choose_view(request):
    """ Выбрать достижение для изменения """
    form = request.form
    achievement_service = AchievementServiceTBot(form=form)
    achievements = achievement_service.all
    template = AchievementsForm(achievements=achievements, view='edit_choose')
    return template


def delete_choose_view(request):
    """ Выбрать достижение для удаления """
    form = request.form
    achievement_service = AchievementServiceTBot(form=form)
    achievements = achievement_service.all
    template = AchievementsForm(achievements=achievements, view='delete_choose')
    return template


__all__ = \
    [
        'list_view',
        'add_view',
        'edit_choose_view',
        'delete_choose_view',
    ]
