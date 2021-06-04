"""
View обязанности.
"""
from app.services.review import CoworkerReviewService
from app.tbot.services import CoworkerAdviceServiceTBot
from app.tbot.services.forms import CoworkerAdvicesForm


def list_view(request):
    """ Показать все достижения в форме """
    review = request.args['review'][0]
    advice_type = request.args['type'][0]
    review = CoworkerReviewService().by_pk(review)
    service = CoworkerAdviceServiceTBot(review=review, advice_type=advice_type)
    advices = service.all
    if advices:
        template = CoworkerAdvicesForm(coworker_advices=advices, advice_type=advice_type, review=review, view='list')
    else:
        template = add_view(request=request)
    return template


def add_view(request):
    """ Добавить одно или несколько достижений в форму """
    review = request.args['review'][0]
    advice_type = request.args['type'][0]
    review = CoworkerReviewService().by_pk(review)
    service = CoworkerAdviceServiceTBot(review=review, advice_type=advice_type)
    advices = service.all
    template = CoworkerAdvicesForm(coworker_advices=advices, advice_type=advice_type, review=review, view='add')
    next_view = service.create_before(list_view)
    return template, next_view


def edit_choose_view(request):
    """ Выбрать достижение для изменения """
    review = request.args['review'][0]
    advice_type = request.args['type'][0]
    review = CoworkerReviewService().by_pk(review)
    service = CoworkerAdviceServiceTBot(review=review, advice_type=advice_type)
    advices = service.all
    template = CoworkerAdvicesForm(coworker_advices=advices, advice_type=advice_type, review=review, view='edit_choose')
    return template


def delete_choose_view(request):
    """ Выбрать достижение для удаления """
    review = request.args['review'][0]
    advice_type = request.args['type'][0]
    review = CoworkerReviewService().by_pk(review)
    service = CoworkerAdviceServiceTBot(review=review, advice_type=advice_type)
    advices = service.all
    template = CoworkerAdvicesForm(coworker_advices=advices, advice_type=advice_type, review=review, view='delete_choose')
    return template


__all__ = ['add_view', 'list_view', 'edit_choose_view', 'delete_choose_view']
