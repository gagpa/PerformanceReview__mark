from typing import Optional, Tuple

from telebot.types import InlineKeyboardMarkup

from app.models import Project
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions import MessageBuilder
from app.tbot.storages import BUTTONS_TEMPLATES


class ProjectForm:
    """ Шаблон формы проектов """
    __message_builder = MessageBuilder()
    model = None

    def __init__(self, model: Optional[Project] = None,
                 can_add: bool = False,
                 can_edit: bool = False,
                 can_del: bool = False,
                 is_name: bool = False,
                 is_description: bool = False,
                 is_contacts: bool = False,
                 ):
        self.can_add = can_add
        self.can_edit = can_edit
        self.can_del = can_del
        self.is_name = is_name
        self.is_description = is_description
        self.is_contacts = is_contacts
        if model:
            self.add(model)

    def add(self, model: Optional[Project]):
        """ Добавить проект в шаблон"""
        self.model = model

    def __create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.can_add:
            if self.is_name:
                self.markup = None
            elif self.is_description:
                self.markup = None
            elif self.is_contacts:
                self.markup = None
        elif self.can_edit:
            if self.is_name:
                row_1 = [BUTTONS_TEMPLATES['project_edit_description'],
                         BUTTONS_TEMPLATES['project_edit_contacts']]
            elif self.is_description:
                row_1 = [BUTTONS_TEMPLATES['project_edit_name'],
                         BUTTONS_TEMPLATES['project_edit_contacts']]
            elif self.is_contacts:
                row_1 = [BUTTONS_TEMPLATES['project_edit_name'],
                         BUTTONS_TEMPLATES['project_edit_description']]
            else:
                row_1 = [BUTTONS_TEMPLATES['project_edit_name'],
                         BUTTONS_TEMPLATES['project_edit_description'],
                         BUTTONS_TEMPLATES['project_edit_contacts']]
            row_2 = [BUTTONS_TEMPLATES['projects']]
            self.markup = InlineKeyboardBuilder.build_with_pk(row_1, row_2, pk=self.model.id)

        return self.markup

    def __create_message_text(self) -> Optional[str]:
        """ Вернуть преобразованное сообщение """
        title = '[Проект]'
        if self.is_name:
            description = 'Отправьте в сообщении название проекта'
        elif self.is_description:
            description = 'Отправьте в сообщении краткое описание проекта и своей роли на нём'
        elif self.is_contacts:
            description = 'Отправьте в сообщении логины коллег кто может оценить'
        elif self.can_edit:
            description = 'Выберите что вы хотите изменить в проекте'
        else:
            description = ''
        text = f'{self.model.name} {self.model.description} {self.model.users}'

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


__all__ = ['ProjectForm']
