from app.services.achievement import get_for_pk, delete
from app.tbot.extensions import MessageManager
from app.tbot.resources.review_form_views.achievements_views import controller_achievements
from app.tbot.services.achievement import edit_wrapper
from app.tbot.services.forms import AchievementForm


def controller_achievement_delete(message):
    """ Удалить достижение """
    pk = message.pk
    achievement = get_for_pk(pk)
    delete(achievement)

    controller_achievements(message=message)


def controller_achievement_edit(message):
    """ Изменить достижение """
    pk = message.pk

    achievement = get_for_pk(pk)
    message.model = achievement
    template = AchievementForm(achievement)
    MessageManager.ask_user(message=message,
                            next_controller=edit_wrapper(controller_achievements),
                            template=template,
                            )


__all__ = \
    [
        'controller_achievement_delete',
        'controller_achievement_edit',
    ]
