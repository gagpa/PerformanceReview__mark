"""
View обязанности.
"""
from app.services.form_review import FormService
from app.services.user import CoworkerService
from app.tbot.services.forms import ReviewForm
from app.tbot.resources.coworker_review_views.form_views import form_view
from app.tbot.services.coworker import CoworkerServiceTBot


def todo_view(request):
    """ Cовет что делать """
    pk = request.pk()
    coworker = request.user
    form_service = FormService()
    coworker_service = CoworkerServiceTBot(coworker)
    form = form_service.by_pk(pk=pk)
    advice = coworker_service.find_advice(form)
    can_edit = bool(advice)
    template = ReviewForm(model=form, can_add=not can_edit, can_edit=can_edit)
    coworker_service.form = form
    return template, coworker_service.give_todo_before(form_view)


def not_todo_view(request):
    """ Cовет что не делать """
    pk = request.pk()
    coworker = request.user
    form_service = FormService()
    coworker_service = CoworkerServiceTBot(coworker)
    form = form_service.by_pk(pk=pk)
    advice = coworker_service.find_advice(form)
    can_edit = bool(advice)
    template = ReviewForm(model=form, can_add=not can_edit, can_edit=can_edit)
    coworker_service.form = form
    return template, coworker_service.give_not_todo_before(form_view)


__all__ = ['todo_view', 'not_todo_view']
