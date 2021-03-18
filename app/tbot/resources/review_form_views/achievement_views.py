from app.models import Form
from app.services.achievement_service import get_for_pk, delete
from app.tbot.resources.review_form_views.achievements_views import controller_achievements
from app.tbot.services import ask_user
from app.tbot.services.achievement_service import edit_wrapper
from app.tbot.services.template_forms import AchievementFormTemplate


def controller_achievement_delete(call, form: Form):
    """

    :param message:
    :param form:
    :return:
    """
    pk = int(call.data.split(' ')[-1])

    achievement = get_for_pk(pk)
    delete(achievement)

    controller_achievements(message=call.message, form=form)


def controller_achievement_edit(call, form: Form):
    """

    :param call:
    :param form:
    :return:
    """
    pk = int(call.data.split(' ')[-1])

    achievement = get_for_pk(pk)
    template = AchievementFormTemplate()
    template.add(achievement)
    ask_user(message=call.message,
             next_controller=edit_wrapper(controller_achievements),
             template=template,
             form=form,
             data=achievement
             )
