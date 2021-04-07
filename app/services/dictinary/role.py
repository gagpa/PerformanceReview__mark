from app.models import Role
from app.services.abc_entity import Entity


class RoleService(Entity):
    """ Роль сервис """

    @property
    def employee(self):
        """ Вернуть роль сотрудника """
        role = self.__session.query(Role).filter_by(name='Employee').first()
        return role

    @property
    def hr(self):
        """ Вернуть роль hr """
        role = self.__session.query(Role).filter_by(name='HR').first()
        return role

    @property
    def lead(self):
        """ Вернуть роль руководителя """
        role = self.__session.query(Role).filter_by(name='Lead').first()
        return role


__all__ = ['RoleService']
