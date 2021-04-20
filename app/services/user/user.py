from app.db import Session
from app.models import User, Department, Role, Position
from app.services.abc_entity import Entity


class UserService(Entity):
    """ Сервис пользователя """
    Model = User

    def by_chat_id(self, chat_id: str) -> User:
        """ Найти в БД пользователя по chat_id """
        return self.by(chat_id=chat_id)

    def by_username(self, username: str) -> User:
        """ Найти в БД пользователя по username """
        return self.by(username=username)

    def create_default(self, chat_id: str, username: str, fullname: str):  # TODO Некомитеть эту функцию
        """ Создать стандартного пользователя гостя """
        departament = Session().query(Department).all()[0]
        position = Session().query(Position).all()[0]
        role = Session().query(Role).filter_by(name='Employee').first()
        user = User(chat_id=chat_id,
                    username=username,
                    fullname=fullname,
                    department=departament,
                    role=role,
                    position=position,
                    )
        Session().add(user)
        Session().commit()
        return user


__all__ = ['UserService']
