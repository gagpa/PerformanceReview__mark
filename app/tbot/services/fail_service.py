from app.models import Form, Fail
from app.services.fail_service import save, create_empty


def add_wrapper(func):
    """
    Декоратор для создания достижений за текущее review.
    """

    def wrapper(message, form: Form):
        for text in message.text.split(';'):
            fail = create_empty(form=form)
            fail.text = text
            save(fail=fail)
        func(form=form, message=message)

    return wrapper


def edit_wrapper(func):
    """

    :param func:
    :return:
    """

    def wrapper(message, form: Form, data: Fail):
        data.text = message.text
        save(fail=data)
        func(form=form, message=message)

    return wrapper
