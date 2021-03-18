from typing import Optional
from telebot.types import InlineKeyboardMarkup


def build_keyboard_for_form(buttons: Optional[list]) -> InlineKeyboardMarkup:
    """
    Создать inline клавиатуру для формы заполнения обязанностей.
    """
    keyboard = InlineKeyboardMarkup()
    for row in buttons:
        keyboard.add(*row)
    return keyboard
