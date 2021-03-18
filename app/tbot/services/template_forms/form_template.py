from app.models import Form
from app.tbot.services.template_forms.achievements_form_template import AchievementsFormTemplate
from app.tbot.services.template_forms.duty_form_template import DutyFormTemplate
from app.tbot.services.template_forms.fails_form_template import FailsFormTemplate
from app.tbot.services.template_forms.projects_form_template import ProjectsFormTemplate


class FormTemplate:
    """
    Шаблон формы анкеты.
    """

    __ORDER = ['duty', 'projects', 'achievements', 'fails']

    def __init__(self):
        self.templates = {
            'achievements': AchievementsFormTemplate(),
            'duty': DutyFormTemplate(),
            'fails': FailsFormTemplate(),
            'projects': ProjectsFormTemplate(),
        }

    def add(self, form: Form):
        """
        Добавить данные из словаря в форму
        :param form:
        :return:
        """
        self.templates['achievements'].add(form.achievements)
        self.templates['duty'].add(form.duty)
        self.templates['fails'].add(form.fails)
        self.templates['projects'].add(form.projects)

    def dump(self):
        """
        Выгрузить строку сообщене.
        :return:
        """
        dump_message = ''
        for name_template in self.__ORDER:
            dump_message += f'{self.templates[name_template].dump()}\n'
        return dump_message
