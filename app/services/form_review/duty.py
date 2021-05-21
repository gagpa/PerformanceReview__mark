from app.db import Session
from app.models import Duty
from app.services.abc_entity import Entity


class DutyService(Entity):
    """ Сервис обязанностей """
    Model = Duty
    model = None
    form = None
    REQUIREMENTS = {'form'}

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
