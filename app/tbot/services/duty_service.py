from app.models import Form
from app.services.duty_service import add, edit


def add_wrapper(func):
    """
    Декоратор для создания обязанности за текущее review.
    """

    def wrapper(message, form: Form):
        duty_model = add(text=message.text, form=form)
        func(message=message, form=form)

    return wrapper


def edit_wrapper(func):
    """
    Декоратор для изменения обязанности за текущее review.
    """

    def wrapper(message, form: Form):
        duty_model = edit(text=message.text, form=form)
        func(message=message, form=form)

    return wrapper
