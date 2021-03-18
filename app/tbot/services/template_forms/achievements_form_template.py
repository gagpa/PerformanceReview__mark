from app.tbot.services.template_forms.achievement_form_template import AchievementFormTemplate
from app.tbot.storages.templates import TEMPLATE, ACHIEVEMENTS_MESSAGE_TEMPLATE


class AchievementsFormTemplate:
    """
    Шаблон формы достижений.
    """

    def __init__(self):
        self.templates = []

    def __validate_achievement(self, achievement: str) -> bool:
        """
        Валидация достижений.
        """
        if achievement:
            return True

        raise AchievementsValidationError

    def add(self, achievements: list):
        """
        Добавить достижения в форму.
        """
        for achievement in achievements:
            template = AchievementFormTemplate()
            template.add(achievement)
            self.templates.append(template)

    def dump(self) -> str:
        """
        Вернуть преобразованное достижения.
        """
        text = ''
        for i, template in enumerate(self.templates):
            text += f'''{TEMPLATE['title'].format(i + 1)}. {template.dump()}\n'''

        title = TEMPLATE['title'].format('[Достижения]')
        message_text = ACHIEVEMENTS_MESSAGE_TEMPLATE.format(title=title,
                                                            description='\n',
                                                            text=text,
                                                            )
        return message_text


class AchievementsValidationError(Exception):
    """
    Исключения ошибки валидции обязанностей.
    """
    pass
