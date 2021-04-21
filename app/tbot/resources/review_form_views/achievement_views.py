from app.services.form_review import AchievementService
from app.tbot.resources.review_form_views.achievements_views import list_view
from app.tbot.services import AchievementServiceTBot
from app.tbot.services.forms import AchievementForm


def delete_view(request):
    """ Удалить достижение """
    pk = request.args['achievement'][0]
    form = request.form
    service = AchievementService(form=form)
    achievement = service.by_pk(pk=pk)
    service.delete(achievement)
    return list_view(request=request)


def edit_view(request):
    """ Изменить достижение """
    pk = request.args['achievement'][0]
    form = request.form
    service = AchievementServiceTBot(form=form)
    achievement = service.by_pk(pk=pk)
    template = AchievementForm(achievement=achievement, view='edit')
    return template, service.update_before(list_view)


__all__ = \
    [
        'delete_view',
        'edit_view',
    ]
