from app.services.achievement import save, create_empty


def add_wrapper(func):
    """ Декоратор для создания достижений за текущее review """

    def wrapper(message):
        for text in message.text.split(';'):
            achievement = create_empty(form=message.form)
            achievement.text = text
            save(achievement=achievement)
        func(message=message)

    return wrapper


def edit_wrapper(func):
    """ Декоратор для изменения достижений за текущее review """

    def wrapper(message, model):
        model.text = message.text
        save(achievement=model)
        func(message=message)

    return wrapper


__all__ = \
    [
        'add_wrapper',
        'edit_wrapper',
    ]
