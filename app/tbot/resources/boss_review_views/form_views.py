from app.services.review import BossReviewService
from app.services.user import BossService
from app.services.dictinary import StatusService
from app.services.form_review import FormService
from app.tbot.resources.boss_review_views.list_forms_views import list_forms_view
from app.tbot.services.forms import ReviewForm, Notification
from app.tbot import notificator


def form_view(request):
    """ Анкета на проврке босса """
    pk = request.args['review'][0]
    review = BossReviewService().by_pk(pk)
    return ReviewForm(form=review.form, have_markup=True, review_type='boss', review=review)


def accept_form_view(request):
    """ Принять """
    if request.args.get('review'):
        pk = request.args['review'][0]
        boss = request.user
        review = BossReviewService().by_pk(pk)
        BossService(boss).accept(review.form)
        for review in review.form.coworker_reviews:
            notificator.notificate(Notification(view='to_coworkers', form=review.form, review=review), review.coworker.chat_id)
    elif request.args.get('form'):
        pk_form = request.args['form'][0]
        form = FormService().by_pk(pk_form)
        StatusService().change_to_coworker_review(form)
        for review in form.coworker_reviews:
            notificator.notificate(Notification(view='to_coworkers', form=form, review=review), review.coworker.chat_id)
    return list_forms_view(request)


def decline_form_view(request):
    """ Отклонить """
    pk = request.args['review'][0]
    review = BossReviewService().by_pk(pk)
    return ReviewForm(form=review.form, have_markup=False, review_type='boss', view='decline', review=review), \
           request.send_args(send_form_view, review=[pk])


def send_form_view(request):
    pk = request.args['review'][0]
    boss = request.user
    text = request.text
    review = BossReviewService().by_pk(pk)
    notificator.notificate(Notification(view='declined'), boss.chat_id)
    notificator.notificate(Notification(view='to_employee', form=review.form, review=review),
                           review.form.user.chat_id)
    BossService(boss).decline(review.form, text)
    return list_forms_view(request)


__all__ = \
    [
        'form_view',
        'accept_form_view',
        'decline_form_view',
    ]
