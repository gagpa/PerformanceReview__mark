from app.models import Achievement
from app.tbot.storages.templates import TEMPLATE, ACHIEVEMENT_MESSAGE_TEMPLATE


class AchievementFormTemplate:
    """
    Шаблон формы достижений.
    """

    def __init__(self):
        self.model = None

    def __validate_achievement(self, achievement: str) -> bool:
        """
        Валидация достижений.
        """
        if achievement:
            return True

        raise AchievementValidationError

    def add(self, achievement: Achievement):
        """
        Добавить достижения в форму.
        """
        self.model = achievement

    def dump(self) -> str:
        """
        Вернуть преобразованное достижения.
        """
        if self.model:
            text = TEMPLATE['text'].format(self.model.text)
        else:
            text = TEMPLATE['text'].format('Не заполнен')
        message_text = ACHIEVEMENT_MESSAGE_TEMPLATE.format(text=text,
                                                           )
        return message_text


class AchievementValidationError(Exception):
    """
    Исключения ошибки валидции обязанностей.
    """
    pass
