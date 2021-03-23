from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tbot.extensions.button_templates import ButtonWithPkTemplate


class InlineKeyboardBuilder:
    """ Сторитель клавиатур """

    @staticmethod
    def build_list(models, button_template):
        """ Построить клавиаутуру списка """
        row_width = 5
        btns = []
        for i, model in enumerate(models):
            btns.append(InlineKeyboardButton(text=button_template.text.format(i + 1),
                                             callback_data=button_template.callback.format(index=model.id)
                                             ))
        markup = InlineKeyboardMarkup(row_width=row_width)
        markup.add(*btns)
        return markup

    @staticmethod
    def build(*rows: list):
        """ Построить клавиатуру по строчно """
        markup = InlineKeyboardMarkup(row_width=3)
        for row in rows:
            btns = []
            for btn in row:
                btns.append(InlineKeyboardButton(text=btn.text,
                                                 callback_data=btn.callback,
                                                 ))
            markup.add(*btns)
        return markup

    @staticmethod
    def build_with_pk(*rows: list, pk: int):
        """ Посторить клавиатуру по строчно с pk сущности """
        markup = InlineKeyboardMarkup(row_width=3)
        for row in rows:
            btns = []
            for btn in row:
                if isinstance(btn, ButtonWithPkTemplate):
                    callback = btn.callback.format(index=pk)
                else:
                    callback = btn.callback
                btns.append(InlineKeyboardButton(text=btn.text,
                                                 callback_data=callback,
                                                 ))
            markup.add(*btns)
        return markup


__all__ = ['InlineKeyboardBuilder']
