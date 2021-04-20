from app.tbot.resources.review_form_views.fails_views import list_view
from app.tbot.services import FailServiceTBot
from app.tbot.services.forms import FailForm


def delete_view(request):
    """ Удлаить провал """
    pk = request.pk()
    form = request.form
    service = FailServiceTBot(form=form)
    fail = service.by_pk(pk=pk)
    service.delete(fail)
    return list_view(request=request)


def edit_view(request):
    """ Изменить провал """
    pk = request.pk()
    form = request.form
    service = FailServiceTBot(form=form)
    fail = service.by_pk(pk=pk)
    template = FailForm(model=fail)
    return template, service.update_before(list_view)


__all__ = \
    [
        'delete_view',
        'edit_view',
    ]
