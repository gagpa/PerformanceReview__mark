from typing import Callable
from typing import Optional

from app.models import Form
from app.tbot import bot
from app.tbot.services.keyboard_builder import build_keyboard_for_form
from app.db import base


def send_message(message, template, buttons: Optional['list'] = None) -> None:
    """
    Отправить новое сообщение пользователю.
    :param message_id:
    :param chat_id:
    :param template:
    :param buttons:
    :return:
    """
    text = template.dump()
    keyboard = build_keyboard_for_form(buttons=buttons) if buttons else None
    message_id = message.message_id
    chat_id = message.chat.id
    # bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode='html')
    bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode='html')


def ask_user(message, form: Form, template, next_controller: Callable,
             buttons: Optional['list'] = None, data: Optional[base] = None) -> None:
    """
    Спросить пользователя.
    :param message:
    :param form:
    :param message_id:
    :param chat_id:
    :param template:
    :param next_controller:
    :param buttons:
    :param data:
    :return:
    """

    send_message(message=message, template=template, buttons=buttons)
    if data:
        bot.register_next_step_handler(message=message, callback=next_controller, form=form, data=data)
    else:
        bot.register_next_step_handler(message=message, callback=next_controller, form=form)
