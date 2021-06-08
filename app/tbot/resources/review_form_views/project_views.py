from app.services.user import UserService
from app.tbot.resources.review_form_views.projects_views import list_view
from app.tbot.services import ProjectsServiceTBot
from app.tbot.services.forms import ProjectForm


def edit_view(request):
    """ Изменить проект """
    pk = request.args['project'][0]
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    return ProjectForm(project=project, view='edit', review_type='write', have_markup=True)


def edit_name_view(request):
    """ Изменить имя проекта """
    pk = request.args['project'][0]
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(project=project, view='edit_name', review_type='write')
    next_view = service.update_name_before(edit_view)
    return template, next_view


def delete_choose_contact_view(request):
    """ Выбрать контакт под удаление """
    pk = request.args['project'][0]
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(project=project, view='delete_choose_contact', review_type='write', have_markup=True)
    return template


def add_contact_in_current_project_view(request):
    """ Добавить контакт в существующий проект """
    pk = request.args['project'][0]
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(project=project, view='edit_coworkers', review_type='write')
    next_view = service.add_contacts_before(edit_view)
    return template, next_view


def delete_contact_view(request):
    """ Удалить контакт """
    pk = request.args['contact'][0]
    project_pk = request.args['project'][0]
    form = request.form
    user = UserService().by_pk(pk=pk)
    service = ProjectsServiceTBot(form=form)
    service.by_pk(project_pk)
    service.del_contact(user)
    return edit_view(request)


def edit_choose_contact_view(request):
    """ Выбрать контакт для изменения """
    pk = request.args['project'][0]
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(project=project, view='edit_choose_contact', review_type='write', have_markup=True)
    return template


def change_contact_view(request):
    """ Поменять контакт на другой """
    pk = request.args['project'][0]
    pk_contact = request.args['contact'][0]
    old_contact = UserService().by_pk(pk_contact)
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(project=project, view='edit_coworkers', review_type='write')
    next_view = service.update_contacts_before(edit_view, old_contact)
    return template, next_view


def contacts_view(request):
    """ Коллеги проекта """
    pk = request.args['project'][0]
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    if project.reviews:
        return ProjectForm(project=project, have_markup=True, view='contacts', review_type='write')
    return add_contact_in_current_project_view(request)


def edit_description_view(request):
    """ Измнить описание проекта """
    pk = request.args['project'][0]
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(project=project, view='edit_description', review_type='write')
    next_view = service.update_description_before(edit_view)
    return template, next_view


def delete_view(request):
    """ Удалить проект """
    pk = request.args['project'][0]
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    service.delete(*project.ratings)
    service.delete(project)
    return list_view(request=request)


def add_view(request):
    """ Добавить новый проект """
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.create(form=form)
    template = ProjectForm(project=project, review_type='write')
    return template, service.add_model(add_name_view)


def add_name_view(request):
    """ Добавить название проекта """
    project = request.model
    text = request.text
    form = request.form
    service = ProjectsServiceTBot(project, form=form)
    template = ProjectForm(project=project, review_type='write')
    service.name = text
    return template, service.add_model(add_description_view)


def add_description_view(request):
    """ Добавить описание проекта """
    project = request.model
    text = request.text
    form = request.form
    service = ProjectsServiceTBot(project, form=form)
    template = ProjectForm(project=project, review_type='write')
    service.description = text
    return template, service.add_model(add_contacts_view)


def add_contacts_view(request):
    """ Добавить контакты проекта """
    project = request.model
    usernames = request.split_text
    form = request.form
    service = ProjectsServiceTBot(project)
    service.add_contacts(usernames)
    return list_view(request=request)


__all__ = \
    [
        'edit_view',
        'edit_name_view',
        'edit_description_view',
        'delete_view',
        'add_view',
        'add_name_view',
        'add_contacts_view',
        'add_description_view',
    ]
