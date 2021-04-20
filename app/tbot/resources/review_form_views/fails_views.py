from app.tbot.services import FailServiceTBot
from app.tbot.services.forms import FailsForm


def list_view(request):
    """ Показать провалы в форме """
    form = request.form
    service = FailServiceTBot(form=form)
    fails = service.all
    can_edit = bool(fails)
    template = FailsForm(models=fails, can_add=True, can_edit=can_edit, can_del=can_edit)
    return template


def add_view(request):
    """ Добавить один или несколько провалов """
    form = request.form
    service = FailServiceTBot(form=form)
    fails = service.all
    template = FailsForm(models=fails, can_add=False, can_del=False, can_edit=False)

    next_controller = service.create_before(list_view)
    return template, next_controller


def edit_choose_view(request):
    """ Выбрать провал для изменения """
    form = request.form
    service = FailServiceTBot(form=form)
    fails = service.all
    template = FailsForm(models=fails, can_add=False, can_edit=True, can_del=False)
    return template


def delete_choose_view(request):
    """ Выбрать провал для удаления """
    form = request.form
    service = FailServiceTBot(form=form)
    fails = service.all
    template = FailsForm(models=fails, can_add=False, can_edit=False, can_del=True)
    return template


__all__ = \
    [
        'list_view',
        'add_view',
        'edit_choose_view',
        'delete_choose_view'
    ]
