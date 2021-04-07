from urllib.parse import urlencode
from typing import Optional


class ButtonTemplate:
    """ Хранилище информации кнопки """

    def __init__(self, callback: str, text: Optional[str] = None, **kwargs):
        self.__text = text or '{}'
        self.__callback = callback
        self.kwargs = kwargs

    def __repr__(self):
        return f'{self.kwargs}'

    def add(self, **kwargs):
        self.kwargs.update(kwargs)

    @property
    def text(self):
        return self.__text

    @property
    def callback(self):
        self.kwargs.update({'callback': self.__callback})
        callback = urlencode(self.kwargs)
        return callback


__all__ = \
    ['ButtonTemplate']
