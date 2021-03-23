from app.services.project import save
from app.services.user import get_for_username as get_user_for_username


def add_wrapper(func):
    """ Декоратор для создания проекта за текущее review """

    def wrapper(message):
        save(project=message.model)
        func(message=message)

    return wrapper


def edit_name_wrapper(func):
    """ Декоратор для обновления названия проекта за текущее review """

    def wrapper(message, model):
        model.name = message.text
        save(model)
        message.pk = model.id
        func(message=message)

    return wrapper


def edit_description_wrapper(func):
    """ Декоратор для обновления описания проекта за текущее review """

    def wrapper(message, model):
        model.description = message.text
        save(model)
        message.message = message
        message.pk = model.id
        func(message=message)

    return wrapper


def edit_contacts_wrapper(func):
    """ Декоратор для обновления контактов проекта за текущее review """

    def wrapper(message, model):
        usernames = message.text.split(';')
        users = []
        for username in usernames:
            user = get_user_for_username(username)
            if user:
                users.append(user)
        if users:
            model.users = users
            save(model)
        message.pk = model.id
        func(message=message)

    return wrapper


__all__ = \
    [
        'add_wrapper',
        'edit_name_wrapper',
        'edit_description_wrapper',
        'edit_contacts_wrapper',
    ]
