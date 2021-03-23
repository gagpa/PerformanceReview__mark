class ButtonTemplate:
    """ Хранилище информации кнопки """

    def __init__(self, text: str, callback: str):
        self.text = text
        self.callback = callback


class ButtonWithPkTemplate:
    """ Хранилище информации кнопки с pk"""
    __DEFAULT_TEMPLATE_CALLBACK = '{index}'

    def __init__(self, text: str, callback: str):
        self.text = text
        self.callback = f'{callback} {self.__DEFAULT_TEMPLATE_CALLBACK}'


class ListButtonTemplate:
    """ Хранилище информации кнопки списка """
    __DEFAULT_TEMPLATE_NAME = '{}'
    __DEFAULT_TEMPLATE_CALLBACK = '{index}'

    def __init__(self, callback: str):
        self.text = self.__DEFAULT_TEMPLATE_NAME
        self.callback = f'{callback} {self.__DEFAULT_TEMPLATE_CALLBACK}'


__all__ = \
    [
        'ButtonTemplate',
        'ButtonWithPkTemplate',
        'ListButtonTemplate',
    ]
