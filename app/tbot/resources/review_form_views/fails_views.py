from app.tbot.services import FailServiceTBot
from app.tbot.services.forms import FailsForm


def list_view(request):
    """ Показать провалы в форме """
    form = request.form
    service = FailServiceTBot(form=form)
    fails = service.all
    if fails:
        can_edit = bool(fails)
        template = FailsForm(fails=fails, view='list')
    else:
        template = add_view(request=request)
    return template


def add_view(request):
    """ Добавить один или несколько провалов """
    form = request.form
    service = FailServiceTBot(form=form)
    fails = service.all
    template = FailsForm(fails=fails, view='add')

    next_controller = service.create_before(list_view)
    return template, next_controller


def edit_choose_view(request):
    """ Выбрать провал для изменения """
    form = request.form
    service = FailServiceTBot(form=form)
    fails = service.all
    template = FailsForm(fails=fails, view='edit_choose')
    return template


def delete_choose_view(request):
    """ Выбрать провал для удаления """
    form = request.form
    service = FailServiceTBot(form=form)
    fails = service.all
    template = FailsForm(fails=fails, view='delete_choose')
    return template


__all__ = \
    [
        'list_view',
        'add_view',
        'edit_choose_view',
        'delete_choose_view'
    ]
