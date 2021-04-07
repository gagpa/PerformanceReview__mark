"""
View обязанности.
"""
from app.services.form_review import DutyService
from app.tbot.services import DutyServiceTBot
from app.tbot.services.forms import DutyForm


def list_view(request):
    """  Показать обязанность в форме """
    form = request.form
    service = DutyService()
    duty = service.by(form=form)
    can_edit = bool(duty)
    template = DutyForm(model=duty, can_add=not can_edit, can_edit=can_edit)
    return template


def add_view(request):
    """ Добавить обязанность """
    template = DutyForm(can_add=False, can_edit=False)
    service = DutyServiceTBot()
    next_view = service.create_before(list_view)
    return template, next_view


def edit_view(request):
    """ Изменить обязанность """
    form = request.form
    service = DutyServiceTBot()
    duty = service.by(form=form)
    template = DutyForm(model=duty, can_add=False, can_edit=False)
    next_view = service.update_before(list_view)
    return template, next_view


__all__ = \
    [
        'list_view',
        'add_view',
        'edit_view',
    ]
