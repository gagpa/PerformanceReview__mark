"""
View обязанности.
"""
from app.services.form_review import DutyService
from app.tbot.resources.review_form_views.duties_views import list_view
from app.tbot.services import DutyServiceTBot
from app.tbot.services.forms import DutyForm


def delete_view(request):
    """ Удалить достижение """
    pk = request.args['duty'][0]
    form = request.form
    service = DutyService(form=form)
    duty = service.by_pk(pk=pk)
    service.delete(duty)
    return list_view(request=request)


def edit_view(request):
    """ Изменить достижение """
    pk = request.args['duty'][0]
    form = request.form
    service = DutyServiceTBot(form=form)
    duty = service.by_pk(pk=pk)
    template = DutyForm(duty=duty, view='edit')
    return template, service.update_before(list_view)


__all__ = \
    [
        'delete_view',
        'edit_view',
    ]
