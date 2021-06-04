from app.services.review import CoworkerReviewService
from app.tbot.resources.coworker_review_views.advices_views import list_view
from app.tbot.services import CoworkerAdviceServiceTBot
from app.tbot.services.forms import CoworkerAdviceForm


def delete_view(request):
    """ Удалить достижение """
    pk = request.args['coworker_advice'][0]
    review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(review)
    service = CoworkerAdviceServiceTBot(review=review, advice_type='todo')
    coworker_advice = service.by_pk(pk=pk)
    service.delete(coworker_advice)
    return list_view(request=request)


def edit_view(request):
    """ Изменить достижение """
    pk = request.args['coworker_advice'][0]
    review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(review)
    service = CoworkerAdviceServiceTBot(review=review, advice_type='todo')
    coworker_advice = service.by_pk(pk=pk)
    template = CoworkerAdviceForm(coworker_advice=coworker_advice, view='edit')
    return template, service.update_before(list_view)


__all__ = \
    [
        'delete_view',
        'edit_view',
    ]
