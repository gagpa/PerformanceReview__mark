from app.services.review import BossReviewService
from app.services.user import BossService
from app.tbot.resources.boss_review_views.list_forms_views import list_forms_view
from app.tbot.services.forms import ReviewForm


def form_view(request):
    """ Анкета на проврке босса """
    pk = request.args['review'][0]
    review = BossReviewService().by_pk(pk)
    return ReviewForm(form=review.form, have_markup=True, review_type='boss', review=review)


def accept_form_view(request):
    """ Принять """
    pk = request.args['review'][0]
    boss = request.user
    review = BossReviewService().by_pk(pk)
    BossService(boss).accept(review.form)
    return list_forms_view(request)


def decline_form_view(request):
    """ Отклонить """
    pk = request.args['review'][0]
    review = BossReviewService().by_pk(pk)
    return ReviewForm(form=review.form, have_markup=False, review_type='boss', review=review), \
           request.send_args(send_form_view, review=[pk])


def send_form_view(request):
    pk = request.args['review'][0]
    boss = request.user
    text = request.text
    review = BossReviewService().by_pk(pk)
    BossService(boss).decline(review.form, text)
    return list_forms_view(request)


__all__ = \
    [
        'form_view',
        'accept_form_view',
        'decline_form_view',
    ]