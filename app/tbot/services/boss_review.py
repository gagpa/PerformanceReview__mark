from app.services.boss_review import add


def add_wrapper(func):
    """ Декоратор для создания комментария босса на форму """

    def wrapper(message, model):
        add(model, message.user, message.text)
        func(message=message)

    return wrapper


__all__ = \
    [
        'add_wrapper',
    ]
