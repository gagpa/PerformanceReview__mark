from app.services.form_review import AchievementService
from app.db import Session
from app.services.validator import Validator


class AchievementServiceTBot(AchievementService):
    """ """

    def create_before(self, func):
        """ Декоратор для создания достижений за текущее review """

        def wrapper(request):
            achievements = []
            for text in request.split_text:
                Validator().validate_text(text, 'form')
                achievements.append(self.create(text=text, form=self.form))
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
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['AchievementServiceTBot']
