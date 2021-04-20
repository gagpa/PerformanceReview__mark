from abc import ABC, abstractmethod

from telebot.types import InlineKeyboardMarkup

from app.tbot.extensions.keyboard_builder import InlineKeyboardBuilder
from app.tbot.extensions.message_builder import MessageBuilder


class Template(ABC):
    """ Шаблон для формирования ответа """
    markup_builder = InlineKeyboardBuilder()
    message_builder = MessageBuilder()

    def __init__(self, **kwargs):
        self.args = kwargs

    @abstractmethod
    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        pass

    @abstractmethod
    def create_message(self) -> str:
        """ Создать сообщение """
        pass

    def dump(self):
        """ Вернуть клавиатуру + сообщение """
        message = self.create_message()
        markup = self.create_markup()
        return message, markup
