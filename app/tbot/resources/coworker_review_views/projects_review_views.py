from app.services.review import CoworkerReviewService
from app.tbot.services.forms import ProjectsForm


def projects_view(request):
    """ Просмотр проектов под оценку """
    review_pk = request.args['review'][0]
    review = CoworkerReviewService().by_pk(review_pk)
    projects = review.projects
    page = int(request.args['pg'][0]) if request.args.get('pg') else 1
    template = ProjectsForm(form=review.advice.form, ratings=review.projects_ratings, review=review, projects=projects,
                            page=page, review_type='coworker', have_markup=True)
    return template


__all__ = ['projects_view']
