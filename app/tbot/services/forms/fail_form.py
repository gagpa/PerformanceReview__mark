from typing import Optional, Tuple

from telebot.types import InlineKeyboardMarkup

from app.models import Fail
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions import MessageBuilder
from app.tbot.storages import BUTTONS_TEMPLATES


class FailForm:
    """ Шаблон формы провала """
    __message_builder = MessageBuilder()
    model = None
    markup = None

    def __init__(self, model: Optional[Fail] = None, can_edit: bool = False):
        self.can_edit = can_edit
        if model:
            self.add(model)

    def add(self, model: Optional[Fail]):
        """ Добавить провал """
        self.model = model

    def __create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.can_edit:
            row = [BUTTONS_TEMPLATES['form']]
            self.markup = InlineKeyboardBuilder.build(row)
        return self.markup

    def __create_message_text(self) -> str:
        """ Вернуть преобразованное сообщение """
        title = '[ПРОВАЛ]'
        if not self.can_edit:
            description = 'Отправьте в сообщении свой провал или перечислите их через ;'
            text = f'{self.model.text}'
        else:
            description = ''
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


__all__ = ['FailForm']
