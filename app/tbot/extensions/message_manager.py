from typing import Callable

from loguru import logger

from app.tbot.extensions.request_serializer import RequestSerializer


class MessageManager:
    """ Класс для управления сообщениями """

    def __init__(self, bot, commands: dict):
        self.bot = bot
        self.commands = commands

    def handle_response(self, message, response):
        """ Обработать ответ """
        if isinstance(response, tuple):
            self.ask_user(message=message, template=response[0], next_view=response[1])
        else:
            self.send_message(message=message, template=response)

    def send_message(self, message, template) -> None:
        """ Отправить новое сообщение пользователю """
        text, markup = template.dump()
        chat_id = message.chat.id
        if message.from_user.is_bot:
            message = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')
        else:
            message = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')
        return message

    def ask_user(self, message, template, next_view: Callable) -> None:
        """ Спросить пользователя """
        self.send_message(message=message, template=template)
        try:
            self.bot.register_next_step_handler(message=message, callback=self.route(next_view))
        except AttributeError:
            logger.error(str(message))
            raise AttributeError

    def route(self, func):
        def wrapper(message):
            request = RequestSerializer(message=message)
            if message.text in self.commands.keys():
                response = self.commands[message.text](request)
            else:
                response = func(request)
            self.handle_response(message, response)

        return wrapper


__all__ = ['MessageManager']
