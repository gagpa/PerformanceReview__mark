from app.services.user.user import UserService
from app.services.dictinary import StatusService


class EmployeeService(UserService):
    """ Сервис сотрудника """

    def send_boss(self, form):
        service = StatusService()
        service.change_to_boss_review(form)


__all__ = ['EmployeeService']
