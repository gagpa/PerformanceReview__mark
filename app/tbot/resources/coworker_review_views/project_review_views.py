from app.services.review import CoworkerReviewService
from app.services.user import CoworkerService
from app.tbot.services.forms import ProjectForm


def project_view(request):
    """ Преокт на оценке """
    proj_rate_pk = request.args['proj_rate'][0]
    rating = CoworkerReviewService().rating_by_pk(proj_rate_pk)
    review = rating.review
    return ProjectForm(have_markup=True, rating=rating, review=review, project=rating.project, review_type='coworker')


def rate_view(request):
    """ Оценить проект """
    proj_rate_pk = request.args['proj_rate'][0]
    rate_pk = request.args['rate'][0]
    CoworkerService().rate(proj_rate_pk=proj_rate_pk, rate_pk=rate_pk)
    return project_view(request=request)


def comment_view(request):
    """ Прокомментировать проект """
    proj_rate_pk = request.args['proj_rate'][0]
    rating = CoworkerReviewService().rating_by_pk(proj_rate_pk)
    review = rating.review
    return ProjectForm(have_markup=False, rating=rating, review=review, project=rating.project, review_type='coworker',
                       view='comment'), \
           request.send_args(save_comment_view, proj_rate=[proj_rate_pk], review=[review.id])


def save_comment_view(request):
    """ Сохранить комментарий """
    proj_rate_pk = request.args['proj_rate'][0]
    comment = request.text
    CoworkerService().comment_on(proj_rate_pk=proj_rate_pk, text=comment)
    return project_view(request=request)


__all__ = \
    [
        'project_view',
        'rate_view',
        'comment_view',
        'save_comment_view'
    ]
