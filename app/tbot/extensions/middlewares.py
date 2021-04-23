from typing import List, Callable


class OrderMiddlewares:
    """ Класс для упорядочивания middlewares """
    ORDER_MIDDLEWARES = []
    __POSSIBLE_TYPES = \
        [
            'message',
            'callback_query',
        ]

    def __init__(self, bot, messages, callbacks):
        self.bot = bot
        self.messages = messages
        self.callbacks = callbacks

    def activate(self):
        """ Активировать """
        self.add_message(self.messages)
        self.add_callbacks_query(self.callbacks)

    def __add(self, handler_type: str, middlewares: List[Callable]):
        """ Добавить middleware """
        for middleware in middlewares:
            self.bot.middleware_handler(update_types=[handler_type])(session_log(middleware))

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
