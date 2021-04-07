from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.template import Template
from app.tbot.services.forms.achievements_form import AchievementsForm
from app.tbot.services.forms.duty_form import DutyForm
from app.tbot.services.forms.fails_form import FailsForm
from app.tbot.services.forms.projects_form import ProjectsForm
from app.tbot.storages import BUTTONS_TEMPLATES


class ReviewForm(Template):
    """ Шаблон формы анкеты """
    __ORDER = ['review_form_duty', 'review_form_projects_list', 'review_form_achievements_list', 'review_form_fails']
    templates = {
        'review_form_achievements_list': AchievementsForm(can_edit=True, can_del=True),
        'review_form_duty': DutyForm(can_add=True),
        'review_form_fails': FailsForm(can_edit=True, can_del=True),
        'review_form_projects_list': ProjectsForm(can_edit=True, can_del=True),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add()

    def add(self):
        """ Добавить данные из словаря в форму """
        self.templates['review_form_achievements_list'].args['models'] = self.args['model'].achievements
        self.templates['review_form_duty'].args['model'] = self.args['model'].duty
        self.templates['review_form_fails'].args['models'] = self.args['model'].fails
        self.templates['review_form_projects_list'].args['models'] = self.args['model'].projects

    def create_markup(self) -> InlineKeyboardMarkup:
        rows = []

        if self.args.get('write_in'):
            rows.append([BUTTONS_TEMPLATES[self.__ORDER[0]], BUTTONS_TEMPLATES[self.__ORDER[1]]])
            rows.append([BUTTONS_TEMPLATES[self.__ORDER[2]], BUTTONS_TEMPLATES[self.__ORDER[3]]])
            rows.append([BUTTONS_TEMPLATES['review_form_send_to_boss']])
            markup = self.markup_builder.build(*rows)
            return markup

        elif self.args.get('on_boss_review'):
            rows.append([BUTTONS_TEMPLATES['boss_review_accept'],
                         BUTTONS_TEMPLATES['boss_review_decline'],
                         ])
            markup = self.markup_builder.build(*rows, pk=self.args['model'].id)
            return markup

        elif self.args.get('on_coworker_review'):
            rows.append([BUTTONS_TEMPLATES['coworker_review_projects'],
                         BUTTONS_TEMPLATES['coworker_review_todo'],
                         BUTTONS_TEMPLATES['coworker_review_not_todo'],
                         ])
            rows.append([BUTTONS_TEMPLATES['coworker_review_form_send_to_hr']])
            markup = self.markup_builder.build(*rows, pk=self.args['model'].id)
            return markup

    def create_message(self) -> str:
        text = ''
        title = '[АНКЕТА]'
        description = f'Review период:{self.args["model"].review_period}\n' \
                      f'Статус формы: {self.args["model"].status.name}'
        for name_template in self.__ORDER:
            text += f'{self.templates[name_template].dump()[0]}\n'
        message_text = self.message_builder.build_message(title=title,
                                                          description=description,
                                                          text=text,
                                                          )
        return message_text


__all__ = ['ReviewForm']
