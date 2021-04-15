from copy import deepcopy
from typing import List, Optional

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


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
            btns.append(InlineKeyboardButton(text=button_template.text.format(i + 1),
                                             callback_data=button_template.callback
                                             ))
        markup = InlineKeyboardMarkup(row_width=row_width)
        markup.add(*btns)

        for row in rows:
            markup.add(*row)

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
    def build_paginator_arrows(button_template, page, max_page, **kwargs):
        """ Постоить клавиатуру пагинатор стрелок """
        left_arw = None
        right_arw = None
        if page != 1:
            left_arw = InlineKeyboardButton(text='⬅', callback_data=button_template.add(pg=page-1, **kwargs).callback)
        if page != max_page:
            right_arw = InlineKeyboardButton(text='➡', callback_data=button_template.add(pg=page+1, **kwargs).callback)
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


__all__ = ['InlineKeyboardBuilder']
