from app.db import Session
from app.models import User, Role
from app.services.user import UserService


class UserServiceTBot(UserService):
    """ """
    model = None

    def add_model(self, func):
        """ """

        def wrapper(request):
            request.model = self.model
            # Session.commit()
            Session.remove()
            response = func(request=request)
            return response

        return wrapper

    @property
    def fullname(self):
        return self.model.fullname

    @fullname.setter
    def fullname(self, text):
        self.model.fullname = text

    @property
    def username(self):
        return self.model.username

    @username.setter
    def username(self, text):
        self.model.username = text

    @property
    def chat_id(self):
        return self.model.chat_id

    @chat_id.setter
    def chat_id(self, text):
        self.model.chat_id = text

    @property
    def position(self):
        return self.model.position

    @position.setter
    def position(self, position):
        if Session.object_session(self.model) is not Session():
            self.model = Session().merge(self.model)
        self.model.position = position

    @property
    def department(self):
        return self.model.department

    @department.setter
    def department(self, department):
        if Session.object_session(self.model) is not Session():
            self.model = Session().merge(self.model)
        self.model.department = department

    @property
    def role(self):
        return self.model.role

    @role.setter
    def role(self, role):
        if Session.object_session(self.model) is not Session():
            self.model = Session().merge(self.model)
        self.model.role = role

    @property
    def boss(self):
        return self.model.boss

    @boss.setter
    def boss(self, text):  # TODO Обдумать .merge()
        boss_login = text.replace('@', '')
        if boss_login != 'нет':
            boss = Session().query(User).filter_by(username=boss_login).one_or_none()
            if boss:
                self.model.boss = boss
            else:
                self.model.boss = None
        else:
            self.model.boss = None

        if Session.object_session(self.model) is not Session():
            self.model = Session().merge(self.model)
        Session().add(self.model)
        Session.commit()


__all__ = ['UserServiceTBot']
