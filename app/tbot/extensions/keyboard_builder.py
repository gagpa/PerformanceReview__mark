from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from copy import deepcopy


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
        markup = InlineKeyboardMarkup(row_width=3)
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
