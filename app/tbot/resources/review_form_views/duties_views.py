"""
View обязанности.
"""
from app.tbot.services import DutyServiceTBot
from app.tbot.services.forms import DutiesForm


def list_view(request):
    """  Показать обязанность в форме """
    form = request.form
    service = DutyServiceTBot(form=form)
    duties = service.all_by(form=form)
    if duties:
        template = DutiesForm(duties=duties, view='list')
    else:
        template = add_view(request=request)
    return template


def add_view(request):
    """ Добавить обязанность """
    form = request.form
    service = DutyServiceTBot(form=form)
    duties = service.all_by(form=form)
    template = DutiesForm(duties=duties, view='add')
    next_view = service.create_before(list_view)
    return template, next_view


def edit_choose_view(request):
    """ Выбрать обязанность для изменения """
    form = request.form
    duty_service = DutyServiceTBot(form=form)
    duties = duty_service.all
    template = DutiesForm(duties=duties, view='edit_choose')
    return template


def delete_choose_view(request):
    """ Выбрать обязанность для удаления """
    form = request.form
    duty_service = DutyServiceTBot(form=form)
    duties = duty_service.all
    template = DutiesForm(duties=duties, view='delete_choose')
    return template


__all__ = \
    [
        'list_view',
        'add_view',
        'edit_choose_view',
        'delete_choose_view'
    ]
