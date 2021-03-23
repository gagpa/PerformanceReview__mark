from typing import List
from typing import Optional, Tuple

from telebot.types import InlineKeyboardMarkup

from app.models import Form
from app.tbot.extensions import InlineKeyboardBuilder
from app.tbot.extensions import MessageBuilder
from app.tbot.storages import BUTTONS_TEMPLATES


class ListFormReview:
    """ Шаблон списка анкет на проверку """
    __message_builder = MessageBuilder()
    models = []

    def __init__(self, forms: List[Form]):
        if forms:
            self.add(forms)

    def add(self, forms: list):
        """ Добавить формы в шаблон """
        if self.models:
            self.models.extend(forms)
        else:
            self.models = forms

    def __create_markup(self) -> Optional[InlineKeyboardMarkup]:
        """ Создать клавиатуру """
        if self.models:
            markup = InlineKeyboardBuilder.build_list(self.models, BUTTONS_TEMPLATES['boss_review_form'])
            return markup

    def __create_message_text(self) -> Optional[str]:
        """ Вернуть преобразованное сообщение """
        title = '[СПИСОК АНКЕТ НА ПРОВЕРКУ]'
        if self.models:
            description = 'Можете выбрать форму подчинённого на проверку.'
            list_data = [f'{self.model.user.fullname}' for self.model in self.models]
            message_text = self.__message_builder.build_list_message(title=title,
                                                                     description=description,
                                                                     list_data=list_data,
                                                                     )
        else:
            description = ''
            text = 'Нет форм на проверку'
            message_text = self.__message_builder.build_message(title=title, description=description, text=text)
        return message_text

    def dump(self) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        """ Вернуть преобразованное данные """
        message_text = self.__create_message_text()
        markup = self.__create_markup()
        return message_text, markup


__all__ = ['ListFormReview']
