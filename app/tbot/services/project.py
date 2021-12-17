from app.db import Session
from app.models import User
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

    def update_contacts_before(self, func, old_contact: User):
        """ Декоратор для обновления контактов в проекте """

        def wrapper(request):
            text = request.text.replace('@', '')
            new_contact = Session().query(User).filter(User.username == text).first()
            if new_contact:
                self.update_contacts(old_contact, new_contact)
            request.add('project', [self.model.id])
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper

    def add_contacts_before(self, func):
        """ Декортаор для добавления контакта в проект """

        def wrapper(request):
            for i, text in enumerate(request.split_text):
                Validator().validate_text(text, 'form')
            self.add_contacts(request.split_text)
            request.add('project', [self.model.id])
            Session.commit()
            Session.remove()
            return func(request=request)

        return wrapper


__all__ = ['ProjectsServiceTBot']
