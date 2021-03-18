from app.models import Duty
from app.tbot.storages.templates import DUTY_MESSAGE_TEMPLATE, TEMPLATE


class DutyFormTemplate:
    """
    Шаблон формы обязанностей.
    """

    def __init__(self):
        self.model = None

    def __validate_duty(self, duty: str) -> bool:
        """
        Валидация обязанностей.
        """
        if duty:
            return True

        raise DutyValidationError

    def add(self, duty: Duty):
        """
        Добавить обязанности в сообщение.
        """
        self.model = duty

    def dump(self) -> str:
        """
        Вернуть преобразованное сообщение.
        """
        title = TEMPLATE['title'].format('[Обязанности]')
        if self.model:
            text = TEMPLATE['text'].format(self.model.text)
        else:
            text = TEMPLATE['text'].format('Не заполнен')

        message_text = DUTY_MESSAGE_TEMPLATE.format(title=title,
                                                    description='\n',
                                                    text=text,
                                                    )
        return message_text


class DutyValidationError(Exception):
    """
    Исключения ошибки валидции обязанностей.
    """
    pass
