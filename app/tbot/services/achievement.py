from app.services.form_review import AchievementService
from app.db import Session


class AchievementServiceTBot(AchievementService):
    """ """

    def create_before(self, func):
        """ Декоратор для создания достижений за текущее review """

        def wrapper(request):
            achievements = [self.create(text=text, form=self.form) for text in request.split_text]
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper

    def update_before(self, func):
        """ Декоратор для изменения достижений за текущее review """

        def wrapper(request):
            text = request.text
            self.update(text=text)
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['AchievementServiceTBot']
