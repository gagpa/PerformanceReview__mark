from typing import Optional, Tuple

from telebot.types import InlineKeyboardMarkup

from app.models import Form
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions import MessageBuilder
from app.tbot.services.forms.achievements_form import AchievementsForm
from app.tbot.services.forms.duty_form import DutyForm
from app.tbot.services.forms.fails_form import FailsForm
from app.tbot.services.forms.projects_form import ProjectsForm
from app.tbot.storages import BUTTONS_TEMPLATES


class ReviewForm:
    """ Шаблон формы анкеты """
    __message_builder = MessageBuilder()
    __ORDER = ['duty', 'projects', 'achievements', 'fails']
    templates = {
        'achievements': AchievementsForm(can_edit=True, can_del=True),
        'duty': DutyForm(can_add=True),
        'fails': FailsForm(can_edit=True, can_del=True),
        'projects': ProjectsForm(can_edit=True, can_del=True),
    }
    model = None
    markup = None

    def __init__(self, form: Optional[Form],
                 on_write: bool = False,
                 on_boss_review: bool = False,
                 on_coworker_review: bool = False,
                 ):
        self.on_boss_review = on_boss_review
        self.on_write = on_write
        self.on_coworker_review = on_coworker_review
        if form:
            self.add(form)

    def add(self, model: Form):
        """ Добавить данные из словаря в форму """
        self.model = model
        self.templates['achievements'].add(model.achievements)
        self.templates['duty'].add(model.duty)
        self.templates['fails'].add(model.fails)
        self.templates['projects'].add(model.projects)

    def __create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        rows = []
        if self.on_write:
            rows.append([BUTTONS_TEMPLATES[self.__ORDER[0]], BUTTONS_TEMPLATES[self.__ORDER[1]]])
            rows.append([BUTTONS_TEMPLATES[self.__ORDER[2]], BUTTONS_TEMPLATES[self.__ORDER[3]]])
            rows.append([BUTTONS_TEMPLATES['send_to_boss']])
            self.markup = InlineKeyboardBuilder.build(*rows)
            return self.markup
        elif self.on_boss_review:
            rows.append([BUTTONS_TEMPLATES['boss_review_accept'],
                         BUTTONS_TEMPLATES['boss_review_decline'],
                         ])
            self.markup = InlineKeyboardBuilder.build_with_pk(*rows, pk=self.model.id)
            return self.markup
        elif self.on_coworker_review:
            rows.append([BUTTONS_TEMPLATES['coworker_review_projects'],
                         BUTTONS_TEMPLATES['coworker_review_todo'],
                         BUTTONS_TEMPLATES['coworker_review_not_todo'],
                         ])
            rows.append([BUTTONS_TEMPLATES['coworker_review_send_to_hr']])
            self.markup = InlineKeyboardBuilder.build_with_pk(*rows, pk=self.model.id)
            return self.markup

    def __create_message_text(self) -> str:
        """ Вернуть преобразованное сообщение """
        text = ''
        title = '[АНКЕТА]'
        description = f'Review период:{self.model.review_period}\n' \
                      f'Статус формы: {self.model.status.name}'
        for name_template in self.__ORDER:
            text += f'{self.templates[name_template].dump()[0]}\n'
        message_text = self.__message_builder.build_message(title=title,
                                                            description=description,
                                                            text=text,
                                                            )
        return message_text

    def dump(self) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        """ Вернуть преобразованное данные """
        message_text = self.__create_message_text()
        markup = self.__create_markup()
        return message_text, markup


__all__ = ['ReviewForm']
