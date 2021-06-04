from app.db import Session
from app.services.form_review import CoworkerAdviceService
from app.services.validator import Validator
from app.models import AdviceType


class CoworkerAdviceServiceTBot(CoworkerAdviceService):
    """  """

    def create_before(self, func):
        """ Декоратор для создания достижений за текущее review """

        def wrapper(request):
            advices = []
            advice_type = Session().query(AdviceType).filter_by(name=self.advice_type).one()
            for text in request.split_text:
                Validator().validate_text(text, 'form')
                advices.append(self.create(text=text, coworker_review=self.review, advice_type=advice_type))
            request.add('type', [self.advice_type])
            request.add('review', [self.review.id])
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper

    def update_before(self, func):
        """ Декоратор для изменения достижений за текущее review """

        def wrapper(request):
            text = request.text
            Validator().validate_text(text, 'form')
            self.update(text=text)
            request.add('type', [self.advice_type])
            request.add('review', [self.review.id])
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['CoworkerAdviceServiceTBot']
