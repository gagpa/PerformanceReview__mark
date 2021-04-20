from app.services.review import CoworkerReviewService
from app.services.user import HRService
from app.tbot.resources.hr_review_views.form_views import decline_view
from app.tbot.resources.hr_review_views.list_forms_views import list_forms_view
from app.tbot.services.forms import ReviewForm, ProjectsForm, ProjectForm


def todo_view(request):
    """ Заполнение """
    pk_review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    advice = review.advice
    next_view = request.send_args(comment_todo_view, review=[review.id])
    return ReviewForm(review_type='hr', advice=advice, form=advice.form), next_view


def comment_todo_view(request):
    comment = request.text
    user = request.user
    pk_review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    HRService(user).comment_on(model=review.advice, text=comment)
    return decline_view(request)


def ratings_view(request):
    """ Оценки """
    pk_review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    projects = review.projects
    page = int(request.args['pg'][0]) if request.args.get('pg') else 1
    return ProjectsForm(form=review.advice.form, ratings=review.projects_ratings, review=review, projects=projects,
                        page=page, review_type='hr', have_markup=True)


def comment_rating_view(request):
    """ Прокомментировать оценку """
    proj_rate_pk = request.args['proj_rate'][0]
    rating = CoworkerReviewService().rating_by_pk(proj_rate_pk)
    review = rating.review
    next_view = request.send_args(save_comment_rating_view, proj_rate=[proj_rate_pk], review=[review.id])
    return ProjectForm(have_markup=False, rating=rating, review=review, project=rating.project, review_type='hr'), \
           next_view


def save_comment_rating_view(request):
    """ Сохранить прокомментированную оценку """
    pk_rating = request.args['proj_rate'][0]
    user = request.user
    HRService(user).comment_rating(pk=int(pk_rating), text=request.text)
    return ratings_view(request)


def send_back_view(request):
    """ Отправить форму обратно """
    pk_review = request.args['review'][0]
    HRService(model=request.user).decline_coworker_review(pk_review)
    return list_forms_view(request)
