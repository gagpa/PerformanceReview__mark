from app.services.user import BossService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ Контроллер списка review начальника """
    boss = request.user
    boss_service = BossService(model=boss)
    forms = boss_service.forms_on_review
    template = ListFormReview(models=forms, on_boss_review=True)
    return template


__all__ = ['list_forms_view']
