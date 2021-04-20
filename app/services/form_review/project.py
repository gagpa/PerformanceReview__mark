from app.models import Form, Project, User
from app.services.abc_entity import Entity
from app.db import Session


class ProjectsService(Entity):
    """ Сервис проектво """
    Model = Project
    model = None
    form = None
    REQUIREMENTS = {}

    @classmethod
    def create_empty(cls, form: Form):
        """ """
        return cls.Model(form=form)

    @property
    def all_text(self) -> list:
        """ """
        models = self.all
        all_text = [model.text for model in models]
        return all_text

    @property
    def all(self) -> list:
        """  """
        models = Session.query(self.Model).filter_by(form=self.form).all()
        return models

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, text):
        self.model.name = text

    @property
    def description(self):
        return self.model.name

    @description.setter
    def description(self, text):
        self.model.description = text

    @property
    def contacts(self):
        return self.model.users

    @contacts.setter
    def contacts(self, contacts):  # TODO Обдумать .merge()
        users = Session().query(User).filter(User.username.in_(contacts)).all()
        if not Session.object_session(self.model):
            self.model = Session().merge(self.model)
        self.model.users = users
        Session().add(self.model)
        Session().commit()
