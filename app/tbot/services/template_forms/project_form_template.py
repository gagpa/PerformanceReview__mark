from app.models import Project
from app.tbot.storages.templates import PROJECT_MESSAGE_TEMPLATE, TEMPLATE


class ProjectFormTemplate:
    """
    Шаблон формы проектов.
    """

    def __init__(self):
        self.model = None

    def __validate_project(self, project: dict) -> bool:
        """
        Валидация провала.
        """
        if project:
            return True

        raise ProjectValidationError

    def add(self, project: Project):
        """
        :param name:
        :param description:
        :param contacts:
        :return:
        """
        self.model = project

    def dump(self) -> str:
        """
        Вернуть преобразованное провалы.
        """
        if self.model:
            title = TEMPLATE['title'].format(self.model.name)
            description = TEMPLATE['text'].format(self.model.description)
            contacts = TEMPLATE['text'].format(self.model.users)
        else:
            title = ''
            description = 'Блок не заполнен'
            contacts = ''
        message_text = PROJECT_MESSAGE_TEMPLATE.format(title=title,
                                                       description=description,
                                                       contacts=contacts,
                                                       )
        return message_text


class ProjectValidationError(Exception):
    """
    Исключения ошибки валидции проекта.
    """
    pass
