from typing import Callable

from loguru import logger
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from app.tbot.extensions.request_serializer import RequestSerializer
from app.tbot.services.user import get_previous, save_user_step
from app.tbot.extensions.keyboard_builder import InlineKeyboardBuilder


class MessageManager:
    """ Класс для управления сообщениями """

    def __init__(self, bot, commands: dict = None, routes: dict = None, permissions: dict = None):
        self.bot = bot
        self.commands = commands
        self.routes = routes
        self.permissions = permissions

    def handle_response(self, request, response, url=None, url_type=None):
        """ Обработать ответ """
        message = request.message
        if isinstance(response, tuple):
            self.ask_user(message=message, template=response[0], next_view=response[1])
        else:
            self.send_message(message=message, template=response)
            if url and url_type:
                save_user_step(request, url, url_type)

    def send_message(self, message, template, general_markup=None) -> None:
        """ Отправить новое сообщение пользователю """
        if template:
            text, markup = template.dump()
            markup = general_markup or markup
            chat_id = message.chat.id
            if message.from_user.is_bot:
                try:
                    if not isinstance(markup, ReplyKeyboardMarkup):
                        message = self.bot.edit_message_text(chat_id=chat_id, message_id=message.id, text=text,
                                                             reply_markup=markup, parse_mode='html')
                    else:
                        message = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')

                except Exception:
                    try:
                        self.bot.delete_message(chat_id=chat_id, message_id=message.id)
                    except Exception:
                        pass
                    finally:
                        message = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')
            else:
                message = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')
            return message

    def ask_user(self, message, template, next_view: Callable) -> None:
        """ Спросить пользователя """
        markup = ReplyKeyboardMarkup()
        markup.add(KeyboardButton(text='Отменить'))
        self.send_message(message=message, template=template, general_markup=markup)
        try:
            self.bot.register_next_step_handler(message=message, callback=self.route(next_view))
        except AttributeError:
            logger.error(str(message))
            raise AttributeError

    def route(self, func):
        def wrapper(message):
            request = RequestSerializer(message=message)
            if message.text == 'Отменить':
                step = get_previous(request)
                user = request.user
                markup = InlineKeyboardBuilder.build_reply_keyboard(self.permissions[user.role.name])
                self.bot.send_message(chat_id=user.chat_id, text='Вы отменили ввод', reply_markup=markup, parse_mode='html')
                if step.url_type == 'callback':
                    response = self.routes[step.text](request)
                else:
                    response = self.commands[step.text](request)
            elif message.text in self.commands.keys():
                response = self.commands[message.text](request)
            else:
                response = func(request)
            self.handle_response(request, response)

        return wrapper


__all__ = ['MessageManager']
