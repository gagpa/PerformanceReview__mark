from app.services.form_review import FormService, ProjectsService
from app.services.review import CoworkerReviewService
from app.services.user import HRService, CoworkerService
from app.tbot.resources.hr_review_views.form_views import decline_view
from app.tbot.services.forms import ReviewForm, ProjectsForm, ProjectForm
from app.tbot.resources.hr_review_views.list_forms_views import list_forms_view
from app.tbot.resources.hr_review_views.form_views import data_form_views


def todo_view(request):
    """ Заполнение """
    pk_advice = request.args['advice'][0]
    pk_form = request.args['form'][0]
    service = FormService()
    service.by_pk(pk=pk_form)
    form_data = service.data_for_hr(pk_advice=pk_advice)
    next_view = request.send_args(comment_todo_view, advice=pk_advice, form=pk_form)
    return ReviewForm(on_hr_review=True, accept=True, todo=True, **form_data), request.send_args(next_view, )


def comment_todo_view(request):
    comment = request.text
    user = request.user
    pk_advice = request.args['advice'][0]
    advice = CoworkerReviewService().by_pk(pk_advice)
    HRService(user).comment_on(model=advice, text=comment)
    return decline_view(request)


def ratings_view(request):
    """ Оценки """
    pk_form = request.args['form'][0]
    pk_coworker = request.args['coworker'][0]
    pk_advice = request.args['advice'][0]
    service = CoworkerService()
    form = FormService().by_pk(pk_form)
    coworker = service.by_pk(pk_coworker)
    projects = service.find_project_to_comment(form)
    ratings = list(map(service.find_comment, projects))
    return ProjectsForm(projects=projects, advice=pk_advice, ratings=ratings, coworker=coworker, form=form, on_hr_review=True)


def comment_rating_view(request):
    """ Прокомментировать оценку """
    pk_project = request.args['project'][0]
    pk_coworker = request.args['cw'][0]
    pk_advice = request.args['adv'][0]
    project = ProjectsService().by_pk(pk_project)
    service = CoworkerService()
    service.by_pk(pk_coworker)
    rating = service.find_comment(project)
    return ProjectForm(project=project, rating=rating, on_hr_review=True), request.send_args(save_comment_rating_view,
                                                                                             form=request.args['f'],
                                                                                             coworker=request.args['cw'],
                                                                                             rating=rating.id,
                                                                                             advice=pk_advice)


def save_comment_rating_view(request):
    """ Сохранить прокомментированную оценку """
    pk_rating = request.args['rating']
    user = request.user
    HRService(user).comment_rating(pk=int(pk_rating), text=request.text)
    return ratings_view(request)


def send_back_view(request):
    """ Отправить форму обратно """
    form_data = data_form_views(request)
    HRService(model=request.user).decline_coworker_review(advice=form_data['advice'], ratings=form_data['ratings'])
    return list_forms_view(request)

