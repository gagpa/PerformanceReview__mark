from app.services.dictinary.rating import RatingService
from app.services.form_review import ProjectsService
from app.services.user import CoworkerService
from app.tbot.services import CoworkerServiceTBot
from app.tbot.services.forms import ProjectForm


def project_view(request):
    """ Преокт на оценке """
    return project_rate_choose_view(request)


def project_rate_choose_view(request):
    """ Выбор оценки проекта """
    pk = request.pk()
    coworker = request.user
    project_service = ProjectsService()
    project = project_service.by_pk(pk=pk)
    coworker_service = CoworkerServiceTBot(coworker, project=project)
    rating = coworker_service.find_rating(project)
    comment = coworker_service.find_comment(project).text
    left_project, right_project = coworker_service.find_right_left_project(project=project)

    template = ProjectForm(model=project, on_rate=True, rating=rating, comment=comment,
                           left_project=left_project, right_project=right_project)
    return template, coworker_service.comment_on_before(project_comment_on_view)


def project_rate_view(request):
    """ Оценить проект """
    pk_rating = request.pk()
    pk_project = request.pk(key='project_pk')
    coworker = request.user

    project = ProjectsService().by_pk(pk=pk_project)
    rating = RatingService().by_pk(pk=pk_rating)
    CoworkerService(coworker).rate_project(project=project, rating=rating)
    request.add('pk', pk_project)
    return project_rate_choose_view(request)


def project_comment_on_view(request):
    """ Прокомментировать проект коллеги """
    return project_rate_choose_view(request)


__all__ = \
    [
        'project_view',
        'project_comment_on_view',
        'project_rate_choose_view',
        'project_rate_view',
    ]
