from app.services.user import CoworkerService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ Контроллер списка review коллеги """
    coworker = request.user
    service = CoworkerService(coworker)
    if request.args.get('asc'):
        if request.args['asc'][0] == 'True':
            is_asc = True
        else:
            is_asc = False
    else:
        is_asc = True
    reviews = service.reviews
    forms = [review.advice.form for review in reviews]
    page = int(request.args['pg'][0]) if request.args.get('pg') else 1
    template = ListFormReview(forms=forms, reviews=reviews, review='coworker', page=page, is_asc=is_asc)
    return template


__all__ = ['list_forms_view']
