from app.models import Status, Form
from app.services.abc_entity import Entity
from app.models import Status
from app.db import Session


class StatusService(Entity):
    """ Статус сервис """
    Model = Status

    @property
    def write_in(self):
        """ Вернуть статус для новой формы """
        return self.by(name='Заполнение анкеты')

    @property
    def boss_review(self):
        """ Получить статус на оценке босса """
        return self.by(name='У руководителя')

    @property
    def coworker_review(self):
        """ Получить статус на оценке коллег """
        return self.by(name='На оценке коллег')

    def change_to_boss_review(self, form: Form):
        """ Сменить статус на проверке у руководителя """
        form = Session.merge(form)
        form.status = self.boss_review
        self.save(form)
        Session.commit()

    def change_to_coworker_review(self, form: Form):
        """ Сменить статус на оценка коллег """
        form = Session.merge(form)
        form.status = self.coworker_review
        self.save(form)
        Session.commit()

    def change_to_write_in(self, form: Form):
        """ Сменить статус на заполнение формы """
        form = Session.merge(form)
        form.status = self.write_in
        self.save(form)
        Session.commit()


__all__ = ['StatusService']
