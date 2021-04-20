from app.services.user.coworker import CoworkerService
from app.db import Session


class CoworkerServiceTBot(CoworkerService):
    """ """
    project = None
    form = None

    def comment_on_before(self, func):
        """ Декоратор для создания проекта за текущее review """

        def wrapper(request):
            text = request.text
            self.comment_on(text=text, project=self.project)
            request.add('pk', self.project.id)
            Session.commit()
            Session.remove()
            return func(request=request)
        return wrapper

    def give_todo_before(self, func):
        """ Декоратор для записи что делать пользвателю"""

        def wrapper(request):
            text = request.text
            self.give_todo(text=text, form=self.form)
            request.add('pk', self.form.id)
            Session.commit()
            Session.remove()
            return func(request=request)
        return wrapper

    def give_not_todo_before(self, func):
        """ Декоратор для записи что делать пользвателю"""

        def wrapper(request):
            text = request.text
            self.give_not_todo(text=text, form=self.form)
            Session.commit()
            Session.remove()
            request.add('pk', self.form.id)
            return func(request=request)
        return wrapper
