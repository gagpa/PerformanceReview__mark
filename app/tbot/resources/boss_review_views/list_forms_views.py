from app.services.user import BossService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ Контроллер списка review начальника """
    boss = request.user
    is_asc = request.is_asc
    page = request.page
    boss_service = BossService(boss)
    reviews = boss_service.reviews
    forms = [review.form for review in reviews]
    return ListFormReview(forms=forms, reviews=reviews, review='boss', page=page, is_asc=is_asc)


__all__ = ['list_forms_view']
