from app.models import CoworkerAdvice, AdviceType
from app.db import Session
from app.services.abc_entity import Entity
from sqlalchemy import asc


class CoworkerAdviceService(Entity):
    """ Сервис провалов """
    Model = CoworkerAdvice
    model = None
    review = None
    advice_type = None
    REQUIREMENTS = {'review', 'advice_type'}

    @property
    def all_text(self) -> list:
        """ """
        models = self.all
        all_text = [model.text for model in models]
        return all_text

    @property
    def all(self) -> list:
        """  """
        models = Session.query(self.Model).\
            join(AdviceType).\
            filter(self.Model.coworker_review == self.review,
                   AdviceType.name == self.advice_type).order_by(asc(self.Model.advice_type)).all()
        return models
