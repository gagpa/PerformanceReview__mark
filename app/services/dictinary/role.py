from app.db import Session
from app.models import Role
from app.services.abc_entity import Entity


class RoleService(Entity):
    """ Роль сервис """

    @property
    def undefined(self):
        """ Вернуть роль сотрудника """
        role = Session().query(Role).filter_by(name='Undefined').first()
        return role

    @property
    def employee(self):
        """ Вернуть роль сотрудника """
        role = Session().query(Role).filter_by(name='Employee').first()
        return role

    @property
    def hr(self):
        """ Вернуть роль hr """
        role = Session().query(Role).filter_by(name='HR').first()
        return role

    @property
    def lead(self):
        """ Вернуть роль руководителя """
        role = Session().query(Role).filter_by(name='Lead').first()
        return role


__all__ = ['RoleService']
