from app.tbot.services.forms import ReviewForm
from app.services.dictinary import StatusService
from app.services.user import EmployeeService
from app.services.form_review import FormService


def form_view(request):
    """ Покзать анкету """
    form = request.form
    form_service = FormService(form)
    status_service = StatusService()
    write_in = form_service.is_current_status(status_service.write_in)
    template = ReviewForm(model=form, write_in=write_in)
    return template


def send_to_boss_view(request):
    """ Отправить руководителю """
    form = request.form
    employee = request.user
    employee_service = EmployeeService(employee)
    status_service = StatusService()
    employee_service.send_boss(form)
    form_service = FormService(form)
    write_in = form_service.is_current_status(status_service.write_in)  # TODO не обновляется form в сессии
    template = ReviewForm(model=form, write_in=write_in)
    return template


__all__ = [
        'form_view',
        'send_to_boss_view',
    ]
