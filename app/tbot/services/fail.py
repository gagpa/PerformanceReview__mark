from app.services.fail import save, create_empty


def add_wrapper(func):
    """ Декоратор для создания провалов за текущее review """

    def wrapper(message):
        for text in message.text.split(';'):
            fail = create_empty(form=message.form)
            fail.text = text
            save(fail=fail)
        func(message=message)

    return wrapper


def edit_wrapper(func):
    """ Декоратор для изменения провала за текущее review """

    def wrapper(message, model):
        model.text = message.text
        save(fail=model)
        func(message=message)

    return wrapper


__all__ = \
    [
        'add_wrapper',
        'edit_wrapper',
    ]
