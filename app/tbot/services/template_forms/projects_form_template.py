from app.tbot.services.template_forms.project_form_template import ProjectFormTemplate
from app.tbot.storages.templates import PROJECTS_MESSAGE_TEMPLATE, TEMPLATE


class ProjectsFormTemplate:
    """
    Шаблон формы проектов.
    """

    def __init__(self):
        self.templates = []

    def __validate_project(self, project: dict) -> bool:
        """
        Валидация провала.
        """
        if project:
            return True

        raise ProjectValidationError

    def add(self, projects: list):
        """
        Добавить проекты в шаблон.
        :param projects: Список с моделями проекта.
        :return:
        """
        for project in projects:
            template = ProjectFormTemplate()
            template.add(project)
            self.templates.append(template)

    def dump(self) -> str:
        """
        Вернуть преобразованное провалы.
        """
        text = ''
        for i, template in enumerate(self.templates):
            text += f'''{TEMPLATE['title'].format(i + 1)}. {template.dump()}\n'''

        title = TEMPLATE['title'].format('[Проекты]')
        message_text = PROJECTS_MESSAGE_TEMPLATE.format(title=title,
                                                        description='\n',
                                                        text=text,
                                                        )
        return message_text


class ProjectValidationError(Exception):
    """
    Исключения ошибки валидции проекта.
    """
    pass
