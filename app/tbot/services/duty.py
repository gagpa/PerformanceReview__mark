from app.services.duty import add, edit


def add_wrapper(func):
    """ Декоратор для создания обязанности за текущее review """

    def wrapper(message):
        add(text=message.text, form=message.form)
        func(message=message)

    return wrapper


def edit_wrapper(func):
    """ Декоратор для изменения обязанности за текущее review """

    def wrapper(message):
        edit(text=message.text, form=message.form)
        func(message=message)

    return wrapper


__all__ = \
    [
        'add_wrapper',
        'edit_wrapper',
    ]
