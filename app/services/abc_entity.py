from abc import ABC

from loguru import logger

from app.db import Session


class Entity(ABC):
    """ Сущность """
    Model = None
    model = None
    REQUIREMENTS = set()

    def __init__(self, model=None, **kwargs):
        self.model = model or type(self).Model
        self.Model = type(model) if model else self.Model

        for key, value in kwargs.items():
            self.__setattr__(key, value)
        if model and self.Model is not type(self).Model:
            logger.error(f'Переданный класс: {self.Model} Ожидаемый класс: {type(self).Model}')
            raise WrongModelError

        for arg in self.REQUIREMENTS:
            if arg not in kwargs.keys():
                print(arg)
                raise ArgumentNotFounded

    def create(self, **kwargs):
        """ """
        self.model = self.Model(**kwargs)
        self.save(self.model)
        return self.model

    def save(self, model):
        """ """
        if not Session.object_session(model):
            model = Session().merge(model)
        Session().add(model)

    def add(self, model):
        """ """
        self.save(model)
        self.model = model

    def save_all(self, *models):
        """ """
        Session().add_all(models)
        Session.commit()

    def delete(self, *models):
        """ """
        for model in models:
            Session().delete(model)
        Session().commit()

    def by_pk(self, pk: int):
        """ """
        return self.by(id=pk)

    def by(self, **kwargs):
        """ """
        self.model = Session().query(self.Model).filter_by(**kwargs).first()
        return self.model

    def all_by(self, **kwargs):
        self.model = Session().query(self.Model).filter_by(**kwargs).all()
        return self.model

    def is_exist(self, **kwargs):
        """ """
        return Session().query(Session().query(self.Model).filter_by(**kwargs).exists()).scalar()

    def update(self, **kwargs):
        """ """
        for key, value in kwargs.items():
            setattr(self.model, key, value)

        Session().add(self.model)


class WrongModelError(Exception):
    pass


class ArgumentNotFounded(Exception):
    pass


__all__ = ['Entity', 'WrongModelError']
