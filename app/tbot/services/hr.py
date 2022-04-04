from app.services.user import HRService
from app.db import Session
from app.services.validator import Validator


class HRServiceTBot(HRService):
    """ """
    advice = None

    def comment_before(self, func):
        """ Декоратор для создания достижений за текущее review """

        def wrapper(request):
            comment = request.text
            Validator().validate_text(comment, 'form')
            comment = None if comment == '+' else comment
            self.advice.hr_comment = comment
            Session().add(self.advice)
            request.add('review', [self.advice.coworker_review.id])
            request.add('type', [self.advice.advice_type.name])
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['HRServiceTBot']
