import datetime
from copy import deepcopy
from math import ceil
from typing import List, Optional

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import telebot_calendar
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from configs.bot_config import OBJECT_PER_PAGE


class InlineKeyboardBuilder:
    """ Сторитель клавиатур """

    @staticmethod
    def build_list(models, button_template, *rows, **kwargs):
        """ Построить клавиаутуру списка """
        row_width = 5
        btns = []
        button_template.add(**kwargs)
        for i, model in enumerate(models):
            button_template.add(pk=model.id)
            btns.append(InlineKeyboardButton(text=button_template.text.format(i + 1),
                                             callback_data=button_template.callback
                                             ))
        markup = InlineKeyboardMarkup(row_width=row_width)
        markup.add(*btns)

        for row in rows:
            markup.add(*row)

        return markup

    @staticmethod
    def build_list_up(button_template, unique_args: List[dict], general_args: Optional[dict] = None, *rows):
        """ Построить клавиатуру списка """
        row_width = 5
        btns = []
        if general_args:
            button_template.add(**general_args)
        for i, args in enumerate(unique_args):
            button_template.add(**args)
            btns.append(InlineKeyboardButton(text=i + 1,
                                             callback_data=button_template.callback
                                             ))
        markup = InlineKeyboardMarkup(row_width=row_width)
        markup.add(*btns)

        for row in rows:
            temp_row = [btn if isinstance(btn, InlineKeyboardButton)
                        else InlineKeyboardButton(text=btn.add(**general_args).text, callback_data=btn.callback)
                        for btn in row]
            markup.add(*temp_row)

        return markup

    @staticmethod
    def build_btns_paginator_arrows(button_template, left_model=None, right_model=None, **kwargs):
        """ Постоить клавиатуру пагинатор стрелок """
        btns = []
        button_template.add(**kwargs)
        if left_model:
            button_template.add(pk=left_model.id)
            btns.append(InlineKeyboardButton(text='⬅', callback_data=button_template.callback))
        if right_model:
            right_btn = deepcopy(button_template)
            right_btn.add(pk=right_model.id)
            btns.append(InlineKeyboardButton(text='➡', callback_data=right_btn.callback))
        return btns

    @staticmethod
    def build_paginator_arrows(button_template, page, count_obj, **kwargs):
        """ Постоить клавиатуру пагинатор стрелок """
        left_arw = None
        right_arw = None
        max_page = ceil(count_obj / OBJECT_PER_PAGE)
        if page != 1:
            left_arw = InlineKeyboardButton(text='⬅', callback_data=button_template.add(pg=page - 1, **kwargs).callback)
        if page != max_page:
            right_arw = InlineKeyboardButton(text='➡',
                                             callback_data=button_template.add(pg=page + 1, **kwargs).callback)
        btns = []
        if left_arw:
            btns.append(left_arw)
        if right_arw:
            btns.append(right_arw)
        return btns

    @staticmethod
    def build_btns(*template_btns, **kwargs):
        btns = []
        for template_btn in template_btns:
            template_btn.add(**kwargs)
            btn = InlineKeyboardButton(text=template_btn.text, callback_data=template_btn.callback)
            btns.append(btn)
        return btns

    @staticmethod
    def build(*rows: list, **kwargs):
        """ Построить клавиатуру по строчно """
        markup = InlineKeyboardMarkup(row_width=5)
        for row in rows:
            btns = []
            for btn in row:
                btn.add(**kwargs)
                btns.append(InlineKeyboardButton(text=btn.text,
                                                 callback_data=btn.callback,
                                                 ))
            markup.add(*btns)
        return markup

    @staticmethod
    def build_calendar(call_data):
        now = datetime.datetime.now()
        # документация по календарю: https://github.com/FlymeDllVa/telebot-calendar
        calendar = telebot_calendar.CallbackData(call_data, "action", "year", "month", "day")
        markup = telebot_calendar.create_calendar(name=calendar.prefix,
                                                  year=now.year,
                                                  month=now.month)
        return markup


__all__ = ['InlineKeyboardBuilder']
