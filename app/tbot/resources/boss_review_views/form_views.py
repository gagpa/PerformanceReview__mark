from app.services.form_review import FormService
from app.tbot.resources.boss_review_views.list_forms_views import list_forms_view
from app.tbot.services import BossServiceTBot
from app.tbot.services.forms import ReviewForm


def form_view(request):
    """ Анкета на проврке босса """
    pk = request.pk()
    form_service = FormService()
    form = form_service.by_pk(pk=pk)
    template = ReviewForm(model=form, on_boss_review=True)

    return template


def accept_form_view(request):
    """ Принять """
    pk = request.pk()
    boss = request.user
    form_service = FormService()
    form = form_service.by_pk(pk=pk)
    boss_service = BossServiceTBot(boss, form=form)
    boss_service.accept(form)
    return list_forms_view(request)


def decline_form_view(request):
    """ Отклонить """
    pk = request.pk()
    boss = request.user
    form_service = FormService()
    form = form_service.by_pk(pk=pk)
    template = ReviewForm(model=form)
    boss_service = BossServiceTBot(boss, form=form)
    boss_service.decline(form, text='')
    return template, boss_service.decline_before(list_forms_view)


__all__ = \
    [
        'form_view',
        'accept_form_view',
        'decline_form_view',
    ]
