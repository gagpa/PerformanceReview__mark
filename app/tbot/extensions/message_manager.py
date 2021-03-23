from typing import Callable

from app.tbot import bot


class MessageManager:
    """ Класс для управления сообщениями """

    @classmethod
    def send_message(cls, message, template) -> None:
        """ Отправить новое сообщение пользователю """
        text, markup = template.dump()
        chat_id = message.chat.id
        bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')
        # message_id = message.message_id
        # bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode='html')

    @classmethod
    def ask_user(cls, message, template, next_controller: Callable) -> None:
        """ Спросить пользователя """
        cls.send_message(message=message, template=template)
        try:
            model = message.model
            bot.register_next_step_handler(message=message, callback=next_controller, model=model)
        except AttributeError:
            bot.register_next_step_handler(message=message, callback=next_controller)


__all__ = ['MessageManager']
