from app.models import Fail
from app.tbot.storages.templates import FAIL_MESSAGE_TEMPLATE, TEMPLATE


class FailFormTemplate:
    """
    Шаблон формы провалов.
    """

    def __init__(self):
        self.model = None

    def __validate_fail(self, fail: str) -> bool:
        """
        Валидация провала.
        """
        if fail:
            return True

        raise FailValidationError

    def add(self, fail: Fail):
        """
        Добавить провалы в форму.
        """
        self.model = fail

    def dump(self) -> str:
        """
        Вернуть преобразованное провалы.
        """

        if self.model:
            text = TEMPLATE['text'].format(self.model.text)
        else:
            text = TEMPLATE['text'].format('Не заполнен')
        message_text = FAIL_MESSAGE_TEMPLATE.format(text=text,
                                                    )
        return message_text


class FailValidationError(Exception):
    """
    Исключения ошибки валидции провала.
    """
    pass
