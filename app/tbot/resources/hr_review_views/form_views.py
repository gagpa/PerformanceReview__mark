from app.services.form_review import FormService
from app.tbot.services.forms import ReviewForm


def form_view(request):
    """  """
    pk_advice = request.args['advice'][0]
    pk_form = request.args['form'][0]
    service = FormService()
    service.by_pk(pk=pk_form)
    form_data = service.data_for_hr(pk_advice=pk_advice)
    return ReviewForm(on_hr_review=True, **form_data)


def accept_view(request):
    """ """
    pk_advice = request.args['advice'][0]
    pk_form = request.args['form'][0]
    service = FormService()
    service.by_pk(pk=pk_form)
    form_data = service.data_for_hr(pk_advice=pk_advice)
    return ReviewForm(on_hr_review=True, accept=True, **form_data)


def decline_view(request):
    """ """
    pk_advice = request.args['advice'][0]
    pk_form = request.args['form'][0]
    service = FormService()
    service.by_pk(pk=pk_form)
    form_data = service.data_for_hr(pk_advice=pk_advice)
    return ReviewForm(on_hr_review=True, decline=True, **form_data)
