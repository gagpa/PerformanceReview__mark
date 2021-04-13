from app.services.form_review import FormService
from app.services.review import CoworkerReviewService
from app.services.user import HRService
from app.tbot.resources.hr_review_views.form_views import decline_view
from app.tbot.services.forms import ReviewForm


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

# def list_rating_view(request):
#     """  """
#     pk_form = request.args['form'][0]
#     pk_coworker = request.args['coworker'][0]
#     form = FormService().by_pk(pk=pk_form)
#     service = CoworkerService()
#     service.by_pk(pk=pk_coworker)
#     projects = service.find_project_to_comment(form)
#     template = ProjectsForm(models=projects, on_hr_review=True)
#     return template
