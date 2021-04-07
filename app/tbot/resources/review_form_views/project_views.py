from app.tbot.resources.review_form_views.projects_views import list_view
from app.tbot.services import ProjectsServiceTBot
from app.tbot.services.forms import ProjectForm


def edit_view(request):
    """ Изменить проект """
    pk = request.pk()
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(model=project, can_edit=True)
    return template


def edit_name_view(request):
    """ Изменить имя проекта """
    pk = request.pk()
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(model=project, can_add=True, is_name=True)
    next_view = service.update_name_before(edit_view)
    return template, next_view


def edit_contacts_view(request):
    """ Изменить контакты к проекту """
    pk = request.pk()
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(model=project, can_add=True, is_contacts=True)
    next_view = service.update_contacts_before(edit_view)
    return template, next_view


def edit_description_view(request):
    """ Измнить описание проекта """
    pk = request.pk()
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    template = ProjectForm(model=project, can_add=True, is_description=True)
    next_view = service.update_description_before(edit_view)
    return template, next_view


def delete_view(request):
    """ Удалить проект """
    pk = request.pk()
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.by_pk(pk=pk)
    service.delete(project)
    return list_view(request=request)


def add_view(request):
    """ Добавить новый проект """
    form = request.form
    service = ProjectsServiceTBot(form=form)
    project = service.create(form=form)
    template = ProjectForm(model=project, can_add=True, is_name=True)
    return template, service.add_model(add_name_view)


def add_name_view(request):
    """ Добавить название проекта """
    model = request.model
    text = request.text
    form = request.form
    service = ProjectsServiceTBot(model, form=form)
    template = ProjectForm(model=model, can_add=True, is_description=True)
    service.name = text
    return template, service.add_model(add_description_view)


def add_description_view(request):
    """ Добавить описание проекта """
    model = request.model
    text = request.text
    form = request.form
    service = ProjectsServiceTBot(model, form=form)
    template = ProjectForm(model=model, can_add=True, is_contacts=True)
    service.description = text
    return template, service.add_model(add_contacts_view)


def add_contacts_view(request):
    """ Добавить контакты проекта """
    model = request.model
    usernames = request.split_text
    form = request.form
    service = ProjectsServiceTBot(model, form=form)
    service.contacts = usernames
    return list_view(request=request)


__all__ = \
    [
        'edit_view',
        'edit_name_view',
        'edit_contacts_view',
        'edit_description_view',
        'delete_view',
        'add_view',
        'add_name_view',
        'add_contacts_view',
        'add_description_view',
    ]
