from copy import copy
from typing import Callable

from loguru import logger
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from app.services.validator import TextValidationError, InvalidTypeValidationError
from app.tbot.extensions.keyboard_builder import InlineKeyboardBuilder
from app.tbot.extensions.request_serializer import RequestSerializer
from app.tbot.services.user import get_previous, save_user_step


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
            message = self.send_message(message=message, template=response)
            if request.user and url and url_type:
                save_user_step(request, url, url_type, message)

    def send_message(self, message, template, general_markup=None):
        """ Отправить новое сообщение пользователю """
        if template:
            text, markup = template.dump()
            another_messages = []
            markup_in_the_end = None
            tags = []
            if len(text) > 4000:
                for start in range(0, len(text), 4000):
                    new_text = text[start:start + 4000]
                    if tags:
                        new_text = f'{"".join([tag.replace("/", "") for tag in tags])}{new_text}'
                    tags = check_tags(new_text)
                    if tags:
                        new_text = f'{new_text}{"".join(tags)}'
                    another_messages.append(new_text)
                text = another_messages.pop(0)
                markup, markup_in_the_end = markup_in_the_end, markup
            markup = general_markup or markup
            chat_id = message.chat.id
            if message.from_user.is_bot:
                try:
                    if not isinstance(markup, ReplyKeyboardMarkup):
                        message = self.bot.edit_message_text(chat_id=chat_id, message_id=message.id, text=text,
                                                             reply_markup=markup, parse_mode='html')
                    else:
                        self.bot.delete_message(chat_id=chat_id, message_id=message.id)
                        message = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup,
                                                        parse_mode='html'
                                                        )
                except Exception:
                    try:
                        self.bot.delete_message(chat_id=chat_id, message_id=message.id)
                    except Exception:
                        pass
                    finally:
                        message = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup,
                                                        parse_mode='html')
            else:
                message = self.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='html')
            if another_messages:
                count_messages = len(another_messages)
                for m in another_messages:
                    if another_messages.index(m) == count_messages - 1:
                        self.bot.send_message(chat_id=chat_id, message_id=message.id, text=m,
                                              reply_markup=markup_in_the_end)
                    else:
                        self.bot.send_message(chat_id=chat_id, message_id=message.id, text=m)
            return message

    def ask_user(self, message, template, next_view: Callable) -> None:
        """ Спросить пользователя """
        markup = ReplyKeyboardMarkup()
        if message.user['is_exist']:
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
            user = request.user
            try:
                if message.user['is_exist'] and message.text == 'Отменить':
                    step = get_previous(request)
                    markup = InlineKeyboardBuilder.build_reply_keyboard(self.permissions[user.role.name])
                    self.bot.send_message(chat_id=user.chat_id, text='Вы отменили ввод', reply_markup=markup,
                                          parse_mode='html')
                    if step.url_type == 'callback':
                        response = self.routes[step.text](request)
                    else:
                        response = self.commands[step.text](request)
                elif message.text in self.commands.keys():
                    response = self.commands[message.text](request)
                else:
                    if message.user['is_exist']:
                        markup = InlineKeyboardBuilder.build_reply_keyboard(self.permissions[user.role.name])
                        self.bot.send_message(chat_id=user.chat_id, text='Данные приняты', reply_markup=markup,
                                              parse_mode='html')
                    response = func(request)

            except InvalidTypeValidationError as e:
                step = get_previous(request)
                markup = InlineKeyboardBuilder.build_reply_keyboard(self.permissions[user.role.name])
                self.bot.send_message(chat_id=user.chat_id, text='‼️ Отправлять можно только текст',
                                      reply_markup=markup,
                                      parse_mode='html')
                if step.url_type == 'callback':
                    response = self.routes[step.text](request)
                else:
                    response = self.commands[step.text](request=request)

            except TextValidationError as e:
                step = get_previous(request)
                markup = InlineKeyboardBuilder.build_reply_keyboard(self.permissions[user.role.name])
                self.bot.send_message(chat_id=user.chat_id,
                                      text=f'‼️ Максимальное количество сиволов {e.args[1]},'
                                           f' а вы отправили {e.args[0]}',
                                      reply_markup=markup,
                                      parse_mode='html')
                if step.url_type == 'callback':
                    response = self.routes[step.text](request)
                else:
                    response = self.commands[step.text](request=request)

            self.handle_response(request, response)

        return wrapper


def check_tags(string):
    brackets_open = ['<i>', '<b>']
    brackets_closed = ['</i>', '</b>']
    stack = []
    for i, char in enumerate(string):
        if i + 3 > len(string):
            break
        sub = string[i: i + 3]
        if sub in brackets_open:
            stack.append(sub)
        if sub in brackets_closed:
            if len(stack) == 0:
                return False
            index = brackets_closed.index(sub)
            open_bracket = brackets_open[index]
            if stack[-1] == open_bracket:
                stack = stack[:-1]
            else:
                return False
    if stack:
        new_stack = []
        for i, item in enumerate(stack):
            if item in brackets_open:
                new_stack.append(brackets_closed[i])
            else:
                new_stack.append(brackets_open[i])
        stack = new_stack
    return stack


__all__ = ['MessageManager']
