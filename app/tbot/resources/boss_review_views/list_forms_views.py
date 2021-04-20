from app.services.user import BossService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ Контроллер списка review начальника """
    boss = request.user
    if request.args.get('asc'):
        if request.args['asc'][0] == 'True':
            is_asc = True
        else:
            is_asc = False
    else:
        is_asc = True
    page = int(request.args['pg'][0]) if request.args.get('pg') else 1
    boss_service = BossService(boss)
    reviews = boss_service.reviews
    forms = [review.form for review in reviews]
    return ListFormReview(forms=forms, reviews=reviews, review='boss', page=page, is_asc=is_asc)


__all__ = ['list_forms_view']
