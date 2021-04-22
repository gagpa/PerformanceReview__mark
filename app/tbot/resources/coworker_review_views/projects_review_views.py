from app.services.review import CoworkerReviewService
from app.tbot.services.forms import ProjectsForm


def projects_view(request):
    """ Просмотр проектов под оценку """
    review_pk = request.args['review'][0]
    review = CoworkerReviewService().by_pk(review_pk)
    page = request.page
    return ProjectsForm(form=review.advice.form,
                        ratings=review.projects_ratings,
                        review=review,
                        projects=review.projects,
                        page=page,
                        review_type='coworker',
                        have_markup=True,
                        )


__all__ = ['projects_view']
