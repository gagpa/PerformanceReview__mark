from app.services.user import CoworkerService
from app.services.form_review import FormService
from app.tbot.services.forms import ProjectsForm


def projects_view(request):
    """ Просмотр проектов под оценку """
    coworker = request.user
    pk = request.pk()
    form = FormService().by_pk(pk=pk)
    projects = CoworkerService(coworker).find_project_to_comment(form)
    template = ProjectsForm(models=projects, on_coworker_review=True)
    return template


__all__ = ['projects_view']
