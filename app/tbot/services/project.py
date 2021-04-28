from app.db import Session
from app.services.form_review import ProjectsService
from app.services.validator import Validator


class ProjectsServiceTBot(ProjectsService):
    """ """

    def add_model(self, func):
        """ """

        def wrapper(request):
            request.model = self.model
            Session.commit()
            Session.remove()
            response = func(request=request)
            return response

        return wrapper

    def create_before(self, func):
        """ Декоратор для создания проекта за текущее review """

        def wrapper(request):
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper

    def update_name_before(self, func):
        """ Декоратор для обновления проекта за текущее review """

        def wrapper(request):
            text = request.text
            Validator().validate_text(text, 'form')
            self.model.name = text
            request.add('project', [self.model.id])
            Session.add(self.model)
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper

    def update_description_before(self, func):
        """ Декоратор для обновления проекта за текущее review """

        def wrapper(request):
            text = request.text
            Validator().validate_text(text, 'project_description')
            self.description = text
            request.add('project', [self.model.id])
            Session.add(self.model)
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper

    def update_contacts_before(self, func):
        """ Декоратор для обновления проекта за текущее review """

        def wrapper(request):
            for text in request.split_text:
                Validator().validate_text(text, 'form')
            self.contacts = request.split_text
            request.add('project', [self.model.id])
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['ProjectsServiceTBot']
