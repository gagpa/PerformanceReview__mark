from app.services.user import CoworkerService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ Контроллер списка review коллеги """
    coworker = request.user
    is_asc = request.is_asc
    page = request.page
    reviews = CoworkerService(coworker).reviews
    forms = [review.form for review in reviews]
    return ListFormReview(forms=forms, reviews=reviews, review='coworker', page=page, is_asc=is_asc)


__all__ = ['list_forms_view']
