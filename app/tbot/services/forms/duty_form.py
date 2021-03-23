from typing import Optional, Tuple

from telebot.types import InlineKeyboardMarkup

from app.models import Duty
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions import MessageBuilder
from app.tbot.storages import BUTTONS_TEMPLATES


class DutyForm:
    """ Шаблон формы обязанностей """
    __message_builder = MessageBuilder()
    markup = None
    model = None

    def __init__(self, model: Optional[Duty] = None, can_add: bool = False, can_edit: bool = False):
        self.can_add = can_add
        self.can_edit = can_edit
        if model:
            self.add(model)

    def add(self, duty: Duty):
        """ Добавить обязанности """
        self.model = duty

    def __create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.can_add:
            row_1 = [BUTTONS_TEMPLATES['duty_add']]
        elif self.can_edit:
            row_1 = [BUTTONS_TEMPLATES['duty_edit']]
        else:
            return
        row_2 = [BUTTONS_TEMPLATES['form']]
        self.markup = InlineKeyboardBuilder.build(row_1, row_2)
        return self.markup

    def __create_message_text(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[ОБЯЗАННОСТИ]'
        if self.can_add:
            description = 'Функционал, который ты выполняешь в ходе своей работы'
            text = self.model.text if self.model else ''
        elif self.can_edit:
            description = 'Внесите изменения или вернитесь к анкете'
            text = self.model.text
        else:
            description = 'Отправьте в сообщении свои обязанности'
            text = ''
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


__all__ = ['DutyForm']
