from typing import Optional
from loguru import logger
from app.services.form_review import FormService
from app.services.user import UserService
from app.services.review import ReviewPeriodService


class RequestSerializer:
    """ Сериализатор ответов от Telegram """

    def __init__(self, message):
        self.__message = message

    def pk(self, key: Optional[str] = None):
        """ Парсинг pk из сообщения и вернуть сериализованные данные """
        try:
            key = key or 'pk'
            pk = self.__message.args[key]
            if isinstance(pk, list):
                pk = [self.str_to_int(item) for item in pk]
                pk = pk[0] if len(pk) == 1 else pk
            elif isinstance(pk, str):
                pk = self.str_to_int
            return pk
        except AttributeError:
            logger.error(self.__message.args, key)
            raise AttributeError

    def str_to_int(self, digit: str):
        """ Конвертировать строку в число """
        if isinstance(digit, str) and not digit.isdigit():
            raise ValueError

        return int(digit)

    @property
    def form(self):
        """ Парсинг form из сообщения и вернуть сериализованные данные """
        if self.__message.form['is_exist']:
            pk = self.__message.form['pk']
            service = FormService()
            form = service.by_pk(pk=pk)
            return form

    @property
    def user(self):
        """ Парсинг user из сообщения и вернуть сериализованные данные """
        if self.__message.user['is_exist']:
            pk = self.__message.user['pk']
            service = UserService()
            user = service.by_pk(pk=pk)
            return user

    @property
    def review_period(self):
        """ """
        if self.__message.review_period['is_active']:
            pk = self.__message.review_period['pk']
            service = ReviewPeriodService()
            review_period = service.by_pk(pk=pk)
            return review_period

    @property
    def session(self):
        """ Парсинг session из сообщения и вернуть сериализованные данные """
        return self.__message.session

    @property
    def review_period(self):
        """ Парсинг review_period из сообщения и вернуть сериализованные данные """
        return self.__message.review_period

    @property
    def text(self):
        """ Парсинг review_period из сообщения и вернуть сериализованные данные """
        return self.__message.text

    @property
    def message(self):
        """  """
        return self.__message

    @property
    def split_text(self):
        """ """
        split_text = self.__message.text.split(';')
        split_text = [text.strip().replace('@', '') for text in split_text]
        return split_text

    @property
    def is_asc(self) -> bool:
        if self.args.get('asc'):
            return not self.args['asc'][0] == 'True'
        else:
            return True

    @property
    def page(self) -> int:
        return int(self.args['pg'][0]) if self.args.get('pg') else 1

    def add(self, key, value):
        try:
            self.__message.args[key] = value
        except AttributeError:
            self.__message.args = {key: value}

    @property
    def args(self):
        """ Запарсить аргументы """
        try:
            return self.__message.args
        except AttributeError:
            return {}

    @staticmethod
    def send_args(func, **kwargs):
        def wrapper(request):
            for key, value in kwargs.items():
                request.add(key, value)
            response = func(request)
            return response
        return wrapper
