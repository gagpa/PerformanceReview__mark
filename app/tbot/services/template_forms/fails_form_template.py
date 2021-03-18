from app.tbot.services.template_forms.fail_form_template import FailFormTemplate
from app.tbot.storages.templates import TEMPLATE, FAILS_MESSAGE_TEMPLATE


class FailsFormTemplate:
    """
    Шаблон формы провалов.
    """

    def __init__(self):
        self.templates = []

    def __validate_fail(self, fail: str) -> bool:
        """
        Валидация провала.
        """
        if fail:
            return True

        raise FailValidationError

    def add(self, fails: list):
        """
        Добавить провалы в форму.
        """
        for fail in fails:
            template = FailFormTemplate()
            template.add(fail)
            self.templates.append(template)

    def dump(self) -> str:
        """
        Вернуть преобразованное провалы.
        """
        text = ''
        for i, template in enumerate(self.templates):
            text += f'''{TEMPLATE['title'].format(i + 1)}. {template.dump()}'''

        title = TEMPLATE['title'].format('[Провалы]')
        message_text = FAILS_MESSAGE_TEMPLATE.format(title=title,
                                                     description='\n',
                                                     text=text,
                                                     )
        return message_text


class FailValidationError(Exception):
    """
    Исключения ошибки валидции провала.
    """
    pass
