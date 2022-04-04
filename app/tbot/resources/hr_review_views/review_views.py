from app.services.form_review import CoworkerAdviceService
from app.services.review import CoworkerReviewService
from app.services.user import HRService
from app.tbot import notificator
from app.tbot.resources.hr_review_views.list_forms_views import list_forms_view
from app.tbot.services import CoworkerAdviceServiceTBot
from app.tbot.services.forms import ProjectsForm, ProjectForm, Notification, CoworkerAdvicesForm, CoworkerAdviceForm
from app.tbot.services.hr import HRServiceTBot


def list_advice_view(request):
    """ Заполнение """
    pk_review = request.args['review'][0]
    advice_type = request.args['type'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    advices = CoworkerAdviceService(review=review, advice_type=advice_type).all
    return CoworkerAdvicesForm(view='hr', review=review, coworker_advices=advices, advice_type=advice_type)


def comment_advice_view(request):
    user = request.user
    pk_review = request.args['review'][0]
    pk_advice = request.args['coworker_advice'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    coworker_advice = CoworkerAdviceServiceTBot(review=review, advice_type='todo').by_pk(pk_advice)
    service = HRServiceTBot(user, advice=coworker_advice)
    return CoworkerAdviceForm(coworker_advice=coworker_advice, view='hr'), \
           service.comment_before(list_advice_view)


def ratings_view(request):
    """ Оценки """
    pk_review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    projects = review.projects
    page = int(request.args['pg'][0]) if request.args.get('pg') else 1
    return ProjectsForm(form=review.form, ratings=review.projects_ratings, review=review, projects=projects,
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
    text = None if request.text == '+' else request.text
    HRService(user).comment_rating(pk=int(pk_rating), text=text)
    return ratings_view(request)


def send_back_view(request):
    """ Отправить форму обратно """
    pk_review = request.args['review'][0]
    review = CoworkerReviewService().by_pk(pk_review)
    HRService(model=request.user).decline_coworker_review(pk_review)
    notificator.notificate(Notification(view='from_hr_to_coworker', form=review.form, review=review),
                           review.coworker.chat_id)
    return list_forms_view(request)
