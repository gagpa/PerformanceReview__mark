"""
Файл с кнопками для клавиатур.
"""

from app.tbot.extensions import ButtonTemplate, ListButtonTemplate, ButtonWithPkTemplate

BUTTONS_TEMPLATES = \
    {
        'send_to_boss': ButtonTemplate('Отправить руководителю', 'send_to_boss'),
        'achievements': ButtonTemplate('Достижения', 'achievements'),
        'achievements_add': ButtonTemplate('Добавить', 'achievements_add'),
        'achievement_delete': ListButtonTemplate('achievement_delete'),
        'achievement_edit': ListButtonTemplate('achievement_edit'),
        'achievements_delete_choose': ButtonTemplate('Удалить', 'achievements_delete_choose'),
        'achievements_edit_choose': ButtonTemplate('Изменить', 'achievements_edit_choose'),

        'boss_review_accept': ButtonWithPkTemplate('Принять', 'boss_review_accept'),
        'boss_review_decline': ButtonWithPkTemplate('На доработку', 'boss_review_decline'),
        'boss_review_form': ListButtonTemplate('boss_review_form'),
        'boss_review_list': ButtonTemplate('Список', 'boss_review_list'),

        'coworker_review_form': ListButtonTemplate('coworker_review_form'),
        'coworker_review_list': ButtonTemplate('Список', 'coworker_review_list'),
        'coworker_review_projects': ButtonTemplate('Оценить проекты', 'coworker_review_projects'),
        'coworker_review_todo': ButtonTemplate('Дать совет', 'coworker_review_todo'),
        'coworker_review_not_todo': ButtonTemplate('Что перестать делать', 'coworker_review_not_todo'),
        'coworker_review_send_to_hr': ButtonTemplate('Отправить HR', 'coworker_review_send_to_hr'),

        'fails': ButtonTemplate('Провалы', 'fails'),
        'fails_add': ButtonTemplate('Добавить', 'fails_add'),
        'fail_delete': ListButtonTemplate('fail_delete'),
        'fail_edit': ListButtonTemplate('fail_edit'),
        'fails_delete_choose': ButtonTemplate('Удалить', 'fails_delete_choose'),
        'fails_edit_choose': ButtonTemplate('Изменить', 'fails_edit_choose'),

        'form': ButtonTemplate('Анкета', 'form'),

        'duty': ButtonTemplate('Обязанности', 'duty'),
        'duty_add': ButtonTemplate('Добавить', 'duty_add'),
        'duty_edit': ButtonTemplate('Изменить', 'duty_edit'),

        'projects': ButtonTemplate('Проекты', 'projects'),
        'project_add': ButtonTemplate('Добавить', 'project_add'),
        'project_delete': ListButtonTemplate('project_delete'),
        'project_edit': ListButtonTemplate('project_edit'),
        'project_edit_name': ButtonWithPkTemplate('Название', 'project_edit_name'),
        'project_edit_description': ButtonWithPkTemplate('Описание', 'project_edit_description'),
        'project_edit_contacts': ButtonWithPkTemplate('Контакты', 'project_edit_contacts'),
        'project_delete_choose': ButtonTemplate('Удалить', 'project_delete_choose'),
        'project_edit_choose': ButtonTemplate('Изменить', 'project_edit_choose'),
    }


__all__ = ['BUTTONS_TEMPLATES']
