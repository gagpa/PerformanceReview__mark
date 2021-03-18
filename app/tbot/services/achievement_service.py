from app.models import Form, Achievement
from app.services.achievement_service import save, create_empty


def add_wrapper(func):
    """
    Декоратор для создания достижений за текущее review.
    """

    def wrapper(message, form: Form):
        for text in message.text.split(';'):
            achievement = create_empty(form=form)
            achievement.text = text
            save(achievement=achievement)
        func(form=form, message=message)

    return wrapper


def edit_wrapper(func):
    """
    Декоратор для изменения достижений за текущее review.
    :param func:
    :return:
    """

    def wrapper(message, form: Form, data: Achievement):
        data.text = message.text
        save(achievement=data)
        func(form=form, message=message)

    return wrapper
