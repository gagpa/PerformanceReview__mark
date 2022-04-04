from app.services.review import HrReviewService
from app.services.user import HRService
from app.tbot.resources.hr_review_views.list_forms_views import list_forms_view
from app.tbot.services.forms import ReviewForm, Notification
from app.tbot import notificator


def form_view(request):
    """  """
    pk = request.args['review'][0]
    service = HrReviewService()
    review = service.by_pk(pk)
    ratings = review.projects_ratings
    on_review = service.is_on_review

    template = ReviewForm(form=review.form, have_markup=on_review, ratings=ratings,
                          review_type='hr', review=review)
    return template


def accept_view(request):
    """ Принять форму """
    review_pk = request.args['review'][0]
    service = HRService(model=request.user)
    review = service.accept_coworker_review(review_pk)
    service = HrReviewService()
    if service.is_last_review(review) and HRService().all():
        notificator.notificate(Notification(view='accept_to_hr', form=review.form, review=review),
                               *[hr.chat_id for hr in HRService().all()])
    return list_forms_view(request)


def decline_view(request):
    """ Отклонить форму """
    pk = request.args['review'][0]
    service = HrReviewService()
    review = service.by_pk(pk)
    ratings = review.projects_ratings
    return ReviewForm(form=review.form, review_type='hr', ratings=ratings, review=review, have_markup=True, decline=True)
