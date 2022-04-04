from app.services.user import BossService
# from app.tbot.extensions import RequestSerializer
from app.db import Session


class BossServiceTBot(BossService):
    """ """

    form = None

    def accept_before(self, func):
        """ Декоратор для создания комментария босса на форму """

        def wrapper(request):
            form = request.form
            self.accept(form=form)
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper

    def decline_before(self, func):
        """ Декоратор для создания комментария босса на форму """

        def wrapper(request):
            text = request.text
            form = request.form
            self.decline(form=form, text=text)
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['BossServiceTBot']
