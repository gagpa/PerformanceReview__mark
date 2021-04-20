from typing import List, Callable

from app.tbot import bot
from app.tbot.middlewares import ORDER_CALLBACK_QUERY_MIDDLEWARES
from app.tbot.middlewares import ORDER_MESSAGE_MIDDLEWARES
from app.db import Session
import random


class OrderMiddlewares:
    """ Класс для упорядочивания middlewares """
    ORDER_MIDDLEWARES = []
    __POSSIBLE_TYPES = \
        [
            'message',
            'callback_query',
        ]

    def activate(self):
        """ Активировать """
        self.add_message(ORDER_MESSAGE_MIDDLEWARES)
        self.add_callbacks_query(ORDER_CALLBACK_QUERY_MIDDLEWARES)

    def __add(self, handler_type: str, middlewares: List[Callable]):
        """ Добавить middleware """
        for middleware in middlewares:
            bot.middleware_handler(update_types=[handler_type])(session_log(middleware))

    def add_message(self, middlewares: List[Callable]):
        """ Добавить middleware сообщений """
        self.__add(handler_type='message', middlewares=middlewares)

    def add_callbacks_query(self, middlewares: List[Callable]):
        """ Добавить middleware callback запросов """
        self.__add(handler_type='callback_query', middlewares=middlewares)


def session_log(func):
    def wrapper(bot_instance, call):
        # print(func.__name__, Session())
        # print(random.randint(1, 10))
        a = func(bot_instance, call)
        # print(Session())
        # print('-'*20)
        return a
    return wrapper


__all__ = ['OrderMiddlewares']
