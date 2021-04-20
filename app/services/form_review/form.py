from app.models import Form, Status
from app.services.abc_entity import Entity
from app.services.review import CoworkerReviewService
from app.services.user import CoworkerService


class FormService(Entity):
    """ Сервис анкеты """
    Model = Form
    REQUIREMENTS = {}

    def change_status(self, status: Status):
        """ Обновить статус формы """
        self.model.status = status
        self.save(self.model)

    def is_current_status(self, status: Status):
        """ Проверить текущий это статус формы """
        return self.model.status.name == status.name

    @staticmethod
    def data_for_hr(pk_advice):
        advice = CoworkerReviewService().by_pk(pk_advice)
        service = CoworkerService(advice.coworker)
        data = \
            {
                'advice': advice,
                'coworker': advice.coworker,
                'form': advice.form,
                'ratings': [service.find_comment(project) for project in service.find_project_to_comment(advice.form)],
            }
        return data
