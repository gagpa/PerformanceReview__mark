from abc import ABC, abstractmethod
from telebot.types import InlineKeyboardMarkup
from typing import List, Optional

from app.tbot.extensions.button_templates import ButtonTemplate
from app.tbot.extensions.keyboard_builder import InlineKeyboardBuilder
from app.tbot.extensions.message_builder import MessageBuilder
from configs.bot_config import OBJECT_PER_PAGE


class Template(ABC):
    """ Шаблон для формирования ответа """

    def __init__(self, **kwargs):
        self.markup_builder = InlineKeyboardBuilder()
        self.message_builder = MessageBuilder()
        self.args = kwargs
        self.ADDITIONAL = []
        self.MESSAGE = ''

    @abstractmethod
    def create_markup(self) -> InlineKeyboardMarkup:
        """ Создать клавиатуру """
        pass

    @abstractmethod
    def create_message(self) -> str:
        """ Создать сообщение """
        pass

    def add_sorting(self, asc: ButtonTemplate, desc: ButtonTemplate, is_asc: bool = True,
                    is_next: bool = True):
        """ """
        template = desc if is_asc else asc
        btns = self.markup_builder.build_btns(template)
        self.extend_keyboard(is_next, *btns)

    def add_paginator(self, paginator, page: int, count_obj: int, is_next: bool = True, **kwargs):
        """ Добавить пагинатор """
        if count_obj > 0:
            btns = self.markup_builder.build_paginator_arrows(paginator, page=page,
                                                              count_obj=count_obj,
                                                              **kwargs)
            self.extend_keyboard(is_next, *btns)

    def add_update(self, update: ButtonTemplate, is_next: bool = True):
        """ """
        btns = self.markup_builder.build_btns(update)
        self.extend_keyboard(is_next, *btns)

    def build_list(self, main_template, unique_args: List[dict],
                   prefix: Optional[str] = None, target: Optional[int] = None, **general_args):
        """ """
        return self.markup_builder.build_list_up(main_template, unique_args, general_args,
                                                 prefix, target, *self.ADDITIONAL)

    def build(self, **kwargs):
        return self.markup_builder.build(*self.ADDITIONAL, **kwargs)

    def build_message(self, title=None, description=None, text=None):
        additional_text = self.message_builder.build_message(title=title, description=description,
                                                             text=text)
        self.MESSAGE = f'{self.MESSAGE}\n{additional_text}'

    def build_list_message(self, title=None, description=None, list_text=None):
        additional_text = self.message_builder.build_list_message(title=title,
                                                                  description=description,
                                                                  list_data=list_text)
        self.MESSAGE = f'{self.MESSAGE}\n{additional_text}'

    def current_row(self, btns):
        """ """
        if self.ADDITIONAL:
            self.ADDITIONAL[-1].extend(list(btns))
        else:
            self.next_row(btns)

    def dump(self):
        """ Вернуть клавиатуру + сообщение """
        message = self.create_message()
        markup = self.create_markup()
        return message, markup

    def extend_keyboard(self, is_next: bool = True, *btns):
        """ """
        self.next_row(btns) if is_next else self.current_row(btns)

    def next_row(self, btns):
        """ """
        self.ADDITIONAL.append(list(btns))

    def cut_per_page(self, models: list, page: int):
        """ Отрезать список под страницу"""
        return models[OBJECT_PER_PAGE * (page - 1): OBJECT_PER_PAGE * page]
