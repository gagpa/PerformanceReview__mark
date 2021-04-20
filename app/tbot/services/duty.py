from app.db import Session
from app.services.form_review import DutyService


class DutyServiceTBot(DutyService):
    """ """

    def create_before(self, func):
        """ Декоратор для создания обязанности за текущее review """

        def wrapper(message):
            self.create(text=message.text, form=message.form)
            Session.commit()
            Session.remove()
            return func(request=message)

        return wrapper

    def update_before(self, func):
        """ Декоратор для изменения обязанности за текущее review """

        def wrapper(request):
            self.update(text=request.text)
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['DutyServiceTBot']
