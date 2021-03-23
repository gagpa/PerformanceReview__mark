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

    def __init__(self, forms: List[Form],
                 on_boss_review: bool = False,
                 on_coworker_review: bool = False,
                 ):
        self.on_boss_review = on_boss_review
        self.on_coworker_review = on_coworker_review
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
            if self.on_boss_review:
                return InlineKeyboardBuilder.build_list(self.models, BUTTONS_TEMPLATES['boss_review_form'])
            elif self.on_coworker_review:
                return InlineKeyboardBuilder.build_list(self.models, BUTTONS_TEMPLATES['coworker_review_form'])

    def __create_message_text(self) -> Optional[str]:
        """ Вернуть преобразованное сообщение """
        title = '[СПИСОК АНКЕТ НА ПРОВЕРКУ]'
        if self.models:
            if self.on_boss_review:
                description = 'Можете выбрать форму подчинённого на проверку.'
                list_data = [f'{self.model.user.fullname}' for self.model in self.models]
                return self.__message_builder.build_list_message(title=title,
                                                                 description=description,
                                                                 list_data=list_data,
                                                                 )
            elif self.on_coworker_review:
                description = 'Можете выбрать форму коллеги на оценку.'
                list_data = [f'{self.model.user.fullname}' for self.model in self.models]
                return self.__message_builder.build_list_message(title=title,
                                                                 description=description,
                                                                 list_data=list_data,
                                                                 )
        else:
            description = ''
            text = 'Нет форм на проверку'
            return self.__message_builder.build_message(title=title, description=description, text=text)

    def dump(self) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        """ Вернуть преобразованное данные """
        message_text = self.__create_message_text()
        markup = self.__create_markup()
        return message_text, markup


__all__ = ['ListFormReview']
