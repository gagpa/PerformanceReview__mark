from app.services.review import HrReviewService
from app.services.user import HRService
from app.tbot.resources.hr_review_views.list_forms_views import list_forms_view
from app.tbot.services.forms import ReviewForm


def form_view(request):
    """  """
    pk = request.args['review'][0]
    service = HrReviewService()
    review = service.by_pk(pk)
    ratings = review.projects_ratings
    on_review = service.is_on_review

    template = ReviewForm(form=review.advice.form, advice=review.advice, have_markup=on_review, ratings=ratings,
                          review_type='hr', review=review)
    return template


def accept_view(request):
    """ Принять форму """
    review_pk = request.args['review'][0]
    HRService(model=request.user).accept_coworker_review(review_pk)
    return list_forms_view(request)


def decline_view(request):
    """ Отклонить форму """
    pk = request.args['review'][0]
    service = HrReviewService()
    review = service.by_pk(pk)
    ratings = review.projects_ratings
    return ReviewForm(form=review.advice.form, review_type='hr', ratings=ratings, review=review, advice=review.advice,
                      have_markup=True, decline=True)