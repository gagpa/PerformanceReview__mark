from urllib.parse import urlencode
from typing import Optional


class ButtonTemplate:
    """ Хранилище информации кнопки """

    def __init__(self, callback: str, text: Optional[str] = None, **kwargs):
        self.__text = text or '{}'
        self.__callback = callback
        self.kwargs = kwargs

    def __repr__(self):
        return f'{self.__text}:{self.__callback}'

    def add(self, **kwargs):
        self.kwargs.update(kwargs)
        return self

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def callback(self):
        self.kwargs.update({'cb': self.__callback})
        callback = urlencode(self.kwargs)
        return callback


__all__ = \
    ['ButtonTemplate']
