"""
Файл с шаблонами сообщений для вывода в Телеграм.
"""

ACHIEVEMENT_MESSAGE_TEMPLATE = '{text}'
ACHIEVEMENTS_MESSAGE_TEMPLATE = '{title}{description}\n{text}'

FAIL_MESSAGE_TEMPLATE = '{text}'
FAILS_MESSAGE_TEMPLATE = '{title}{description}\n{text}'

PROJECT_MESSAGE_TEMPLATE = '{title}\n{description}\n{contacts}'
PROJECTS_MESSAGE_TEMPLATE = '{title}{description}\n{text}'

DUTY_MESSAGE_TEMPLATE = '{title}{description}\n{text}'

TEMPLATE = {
    'title': '<b>{}</b>',
    'description': '<i>{}</i>',
    'text': '{}',
    }
