from app.models import Form, Project
from app.services.project_service import save
from app.services.user_service import get_for_username as get_user_for_username


def add_wrapper(func):
    """
    Декоратор для создания проекта за текущее review.
    """

    def wrapper(message, form: Form, project: Project):
        project_model = save(project=project)
        func(form=form, message=message)

    return wrapper


def edit_name_wrapper(func):
    """
    Декоратор для обновления проекта за текущее review.
    """

    def wrapper(message, form: Form, data: Project):
        data.name = message.text
        save(data)
        message.message = message
        message.data = str(data.id)
        func(form=form, call=message)

    return wrapper


def edit_description_wrapper(func):
    """
    Декоратор для обновления проекта за текущее review.
    """

    def wrapper(message, form: Form, data: Project):
        data.description = message.text
        save(data)
        message.message = message
        message.data = str(data.id)
        func(form=form, call=message)

    return wrapper


def edit_contacts_wrapper(func):
    """
    Декоратор для обновления проекта за текущее review.
    """

    def wrapper(message, form: Form, data: Project):
        usernames = message.text.split(';')
        users = []
        for username in usernames:
            user = get_user_for_username(username)
            if user:
                users.append(user)
        if users:
            data.users = users
            save(data)

        message.message = message
        message.data = str(data.id)
        func(form=form, call=message)
    return wrapper
