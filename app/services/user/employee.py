from app.services.user.user import UserService
from app.services.user.boss import BossService
from app.services.dictinary import StatusService
from app.services.review import BossReviewService
from app.db import Session


class EmployeeService(UserService):
    """ Сервис сотрудника """

    def send_boss(self, form):
        service = StatusService()
        service.change_to_boss_review(form)
        boss_service = BossReviewService()
        if not boss_service.is_exist(form=form):
            if form.user.boss:
                Session().add(boss_service.create(form=form, boss=form.user.boss))
            else:
                BossService().accept(form=form)
                Session().add(form)
            Session.commit()


__all__ = ['EmployeeService']
