from app.services.form_review import FormService
from app.services.dictinary import StatusService
from app.tbot.services.forms import ReviewForm
from app.services.user import CoworkerService


def form_view(request):
    """ Анкета на проврке коллеги """
    pk = request.pk()
    form_service = FormService()
    form = form_service.by_pk(pk)
    status_service = StatusService()
    on_coworker_review = form_service.is_current_status(status_service.coworker_review)
    template = ReviewForm(model=form, on_coworker_review=on_coworker_review)
    return template


def send_to_hr(request):
    """ Отправить HR """
    return form_view(request=request)


__all__ = ['form_view', 'send_to_hr']
