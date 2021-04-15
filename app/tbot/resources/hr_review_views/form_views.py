from app.services.form_review import FormService
from app.services.user import HRService
from app.tbot.resources.hr_review_views.list_forms_views import list_forms_view
from app.tbot.services.forms import ReviewForm


def data_form_views(request) -> dict:
    """ Запарсить и обработать необходимую информация для form_view """
    pk_advice = request.args['advice'][0]
    pk_form = request.args['form'][0]
    service = FormService()
    service.by_pk(pk=pk_form)
    form_data = service.data_for_hr(pk_advice=pk_advice)
    return form_data


def form_view(request):
    """  """
    form_data = data_form_views(request)
    return ReviewForm(on_hr_review=True, **form_data)


def accept_view(request):
    """ Принять форму """
    form_data = data_form_views(request)
    HRService(model=request.user).accept_coworker_review(advice=form_data['advice'], ratings=form_data['ratings'])
    return list_forms_view(request)


def decline_view(request):
    """ Отклонить форму """
    form_data = data_form_views(request)
    return ReviewForm(on_hr_review=True, decline=True, **form_data)
