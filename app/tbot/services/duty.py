from app.db import Session
from app.services.form_review import DutyService
from app.services.validator import Validator


class DutyServiceTBot(DutyService):
    """ """

    def create_before(self, func):
        """ Декоратор для создания обязанности за текущее review """

        def wrapper(request):
            duties = []
            for text in request.split_text:
                Validator().validate_text(text, 'form')
                duties.append(self.create(text=text, form=self.form))
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper

    def update_before(self, func):
        """ Декоратор для изменения обязанности за текущее review """

        def wrapper(request):
            text = request.text
            Validator().validate_text(text, 'form')
            self.update(text=text)
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['DutyServiceTBot']
