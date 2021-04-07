from app.models import Form, User, ReviewPeriod, Status
from app.services.abc_entity import Entity


class FormService(Entity):
    """ Сервис анкеты """
    Model = Form
    REQUIREMENTS = {}

    def change_status(self, status: Status):
        """ Обновить статус формы """
        self.model.status = status
        self.save(self.model)

    def is_current_status(self, status):
        """ Проверить текущий это статус формы """
        return self.model.status.name == status.name
