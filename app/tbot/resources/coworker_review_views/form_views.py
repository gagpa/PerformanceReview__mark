from app.services.review import CoworkerReviewService
from app.services.user import CoworkerService, HRService
from app.tbot.resources.coworker_review_views.list_forms_views import list_forms_view
from app.tbot.services.forms import ReviewForm, Notification
from app.tbot import notificator


def form_view(request):
    """ Анкета на проврке коллеги """
    pk = request.args['review'][0]
    service = CoworkerReviewService()
    review = service.by_pk(pk)
    ratings = review.projects_ratings
    on_review = service.is_on_review
    template = ReviewForm(form=review.form, have_markup=on_review, ratings=ratings,
                          review_type='coworker', review=review)
    return template


def send_to_hr(request):
    """ Отправить HR """
    pk = int(request.args['review'][0])
    CoworkerService(request.user).send_hr(pk)
    review = CoworkerReviewService().by_pk(pk)
    if HRService().all():
        notificator.notificate(Notification(view='to_hr', form=review.form, review=review),
                               *[hr.chat_id for hr in HRService().all()])
    return list_forms_view(request=request)


__all__ = ['form_view', 'send_to_hr']
