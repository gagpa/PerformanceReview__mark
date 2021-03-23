from typing import List
from typing import Optional, Tuple

from telebot.types import InlineKeyboardMarkup

from app.models import Project
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions import MessageBuilder
from app.tbot.services.forms.project_form import ProjectForm
from app.tbot.storages import BUTTONS_TEMPLATES


class ProjectsForm:
    """ Шаблон формы проектов """
    __message_builder = MessageBuilder()
    models = []
    templates = []
    markup = None

    def __init__(self, models: List[Project] = None,
                 can_add: bool = False,
                 can_edit: bool = False,
                 can_del: bool = False,
                 ):
        self.can_add = can_add
        self.can_edit = can_edit
        self.can_del = can_del
        if models:
            self.add(models)

    def add(self, data: List[Project]):
        """ Добавить проекты в шаблон """
        self.models = data
        for project in self.models:
            self.templates.append(ProjectForm(project))

    def __create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        rows = []
        if self.can_edit and self.can_del:
            row = [BUTTONS_TEMPLATES['project_add']]
            rows.append(row)
            row = [BUTTONS_TEMPLATES['project_edit_choose'], BUTTONS_TEMPLATES['project_delete_choose']]
            rows.append(row)
            row = [BUTTONS_TEMPLATES['form']]
            rows.append(row)
            self.markup = InlineKeyboardBuilder.build(*rows)
        elif self.can_add:
            row = [BUTTONS_TEMPLATES['project_add']]
            rows.append(row)
            row = [BUTTONS_TEMPLATES['form']]
            rows.append(row)
            self.markup = InlineKeyboardBuilder.build(*rows)
        elif self.can_del:
            btn = BUTTONS_TEMPLATES['project_delete']
            self.markup = InlineKeyboardBuilder.build_list(self.models, btn)
        elif self.can_edit:
            btn = BUTTONS_TEMPLATES['project_edit']
            self.markup = InlineKeyboardBuilder.build_list(self.models, btn)
        return self.markup

    def __create_message_text(self) -> Optional[str]:
        """ Вернуть преобразованное сообщение """

        title = '[ПРОЕКТЫ]'
        if self.models:
            description = 'Перечислите проекты, которые ты выполнял или измените данные'
            list_data = [f'{model.name}\n{model.description} {model.users}' for model in self.models]
        else:
            description = 'Перечислите проекты, которые ты выполнял'
            list_data = None
        message_text = self.__message_builder.build_list_message(title=title,
                                                                 description=description,
                                                                 list_data=list_data,
                                                                 )
        return message_text

    def dump(self) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        """ Вернуть преобразованное данные """
        message_text = self.__create_message_text()
        markup = self.__create_markup()
        return message_text, markup


__all__ = ['ProjectsForm']
