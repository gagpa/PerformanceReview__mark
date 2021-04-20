from app.services.user import CoworkerService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ Контроллер списка review коллеги """
    coworker = request.user
    service = CoworkerService(coworker)
    forms = service.forms_on_review
    template = ListFormReview(models=forms, on_coworker_review=True)
    return template


__all__ = ['list_forms_view']
