from app.services.review import CoworkerReviewService
from app.services.user import CoworkerService
from app.tbot.resources.coworker_review_views.list_forms_views import list_forms_view
from app.tbot.services.forms import ReviewForm


def form_view(request):
    """ Анкета на проврке коллеги """
    pk = request.args['review'][0]
    service = CoworkerReviewService()
    review = service.by_pk(pk)
    ratings = review.projects_ratings
    on_review = service.is_on_review

    template = ReviewForm(form=review.advice.form, advice=review.advice, have_markup=on_review, ratings=ratings,
                          review_type='coworker', review=review)
    return template


def send_to_hr(request):
    """ Отправить HR """
    CoworkerService(request.user).send_hr(int(request.args['review'][0]))
    return list_forms_view(request=request)


__all__ = ['form_view', 'send_to_hr']
