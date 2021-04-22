"""
View обязанности.
"""
from app.db import Session
from app.services.review import CoworkerReviewService
from app.tbot.resources.coworker_review_views.form_views import form_view
from app.tbot.services.forms import ReviewForm


def todo_view(request):
    """ Cовет что делать """
    pk_review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    template = ReviewForm(form=review.advice.form, advice=review.advice, review_type='coworker',
                          ratings=review.projects_ratings, view='todo')
    return template, request.send_args(save_todo_view, review=[review.id])


def save_todo_view(request):
    pk_review = request.args['review'][0]
    text = request.text
    review = CoworkerReviewService().by_pk(pk_review)
    advice = review.advice
    advice.todo = text
    Session().add(advice)
    Session.commit()
    return form_view(request)


def not_todo_view(request):
    """ Cовет что не делать """
    pk_review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    template = ReviewForm(form=review.advice.form, advice=review.advice, review_type='coworker',
                          ratings=review.projects_ratings, view='not todo')
    return template, request.send_args(save_not_todo_view, review=[review.id])


def save_not_todo_view(request):
    pk_review = request.args['review'][0]
    text = request.text
    review = CoworkerReviewService().by_pk(pk_review)
    advice = review.advice
    advice.not_todo = text
    Session().add(advice)
    Session.commit()
    return form_view(request)


__all__ = ['todo_view', 'not_todo_view']
