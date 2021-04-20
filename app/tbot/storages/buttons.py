"""
Файл с кнопками для клавиатур.
"""

from app.tbot.extensions import ButtonTemplate

BUTTONS_TEMPLATES = \
    {
        'review_form_send_to_boss': ButtonTemplate('review_form_send_to_boss', 'Отправить руководителю'),
        'review_form_achievements_list': ButtonTemplate('review_form_achievements_list', 'Достижения'),
        'review_form_achievements_add': ButtonTemplate('review_form_achievements_add', 'Добавить'),
        'review_form_achievement_delete': ButtonTemplate('review_form_achievement_delete'),
        'review_form_achievement_edit': ButtonTemplate('review_form_achievement_edit'),
        'review_form_achievements_delete_choose': ButtonTemplate('review_form_achievements_delete_choose', 'Удалить'),
        'review_form_achievements_edit_choose': ButtonTemplate('review_form_achievements_edit_choose', 'Изменить'),

        'boss_review_accept': ButtonTemplate('boss_review_accept', 'Принять'),
        'boss_review_decline': ButtonTemplate('boss_review_decline', 'На доработку'),
        'boss_review_form': ButtonTemplate('boss_review_form'),
        'boss_review_list': ButtonTemplate('boss_review_list', '« К списку'),
        'boss_review_update_list': ButtonTemplate('boss_review_list', '↻'),
        'boss_review_sort_asc': ButtonTemplate('boss_review_list', '🔺').add(asc=True),
        'boss_review_sort_desc': ButtonTemplate('boss_review_list', '🔻').add(asc=False),

        'coworker_review_form': ButtonTemplate('coworker_review_form', 'Анкета'),
        'coworker_review_list': ButtonTemplate('coworker_review_list', '« К списку'),
        'coworker_projects': ButtonTemplate('coworker_projects', 'Оценить проекты'),
        'coworker_project': ButtonTemplate('coworker_project'),
        'coworker_rate': ButtonTemplate('coworker_rate', 'Оценить'),
        'coworker_back_form': ButtonTemplate('coworker_review_form', '« К форме'),
        'coworker_back_projects': ButtonTemplate('coworker_projects', '« К проектам'),
        'coworker_comment': ButtonTemplate('coworker_comment', 'Прокомментировать'),
        'coworker_review_todo': ButtonTemplate('coworker_review_todo', 'Что делать'),
        'coworker_review_not_todo': ButtonTemplate('coworker_review_not_todo', 'Что не делать'),
        'coworker_review_form_send_to_hr': ButtonTemplate('coworker_review_form_send_to_hr', 'Отправить HR'),
        'coworker_review_sort_asc': ButtonTemplate('coworker_review_list', '🔺').add(asc=True),
        'coworker_review_sort_desc': ButtonTemplate('coworker_review_list', '🔻').add(asc=False),
        'coworker_review_update_list': ButtonTemplate('coworker_review_list', '↻'),

        'review_form_fails': ButtonTemplate('review_form_fails', 'Провалы'),
        'review_form_fails_add': ButtonTemplate('review_form_fails_add', 'Добавить'),
        'review_form_fail_delete': ButtonTemplate('review_form_fail_delete'),
        'review_form_fail_edit': ButtonTemplate('review_form_fail_edit'),
        'review_form_fails_delete_choose': ButtonTemplate('review_form_fails_delete_choose', 'Удалить'),
        'review_form_fails_edit_choose': ButtonTemplate('review_form_fails_edit_choose', 'Изменить'),

        'review_form': ButtonTemplate('review_form', '« К анкете'),

        'review_form_duty': ButtonTemplate('review_form_duty', 'Обязанности'),
        'review_form_duty_add': ButtonTemplate('review_form_duty_add', '✍️'),
        'review_form_duty_edit': ButtonTemplate('review_form_duty_edit', '✍️'),

        'review_form_projects_list': ButtonTemplate('review_form_projects_list', 'Проекты'),
        'review_form_project_add': ButtonTemplate('review_form_project_add', 'Добавить'),
        'review_form_project_delete': ButtonTemplate('review_form_project_delete'),
        'review_form_project_edit': ButtonTemplate('review_form_project_edit'),
        'review_form_project_edit_name': ButtonTemplate('review_form_project_edit_name', 'Название'),
        'review_form_project_edit_description': ButtonTemplate('review_form_project_edit_description', 'Описание'),
        'review_form_project_edit_contacts': ButtonTemplate('review_form_project_edit_contacts', 'Контакты'),
        'review_form_project_delete_choose': ButtonTemplate('review_form_project_delete_choose', 'Удалить'),
        'review_form_project_edit_choose': ButtonTemplate('review_form_project_edit_choose', 'Изменить'),
        'review_form_back_projects_list': ButtonTemplate('review_form_projects_list', '« К Проектам'),

        'hr_review_list': ButtonTemplate('hr_review_list', '« К списку'),
        'hr_review_form': ButtonTemplate('hr_review_form'),
        'hr_review_accept': ButtonTemplate('hr_review_accept', 'Принять'),
        'hr_review_decline': ButtonTemplate('hr_review_decline', 'Отклонить'),
        'hr_review_todo': ButtonTemplate('hr_review_todo', 'TODO'),
        'hr_review_ratings': ButtonTemplate('hr_review_ratings', 'Оценки'),
        'hr_review_back_to_form': ButtonTemplate('hr_review_form', '« Назад'),
        'hr_review_comment_rating': ButtonTemplate('hr_review_comment_rating'),
        'hr_review_back_to_decline': ButtonTemplate('hr_review_decline', '« Назад'),
        'hr_review_send_back': ButtonTemplate('hr_review_send_back', 'Вернуть форму'),
        'hr_review_update_list': ButtonTemplate('hr_review_list', 'Обновить список'),
        'hr_review_sort_asc': ButtonTemplate('hr_review_list', '🔺').add(asc=True),
        'hr_review_sort_desc': ButtonTemplate('hr_review_list', '🔻').add(asc=False)
    }

__all__ = ['BUTTONS_TEMPLATES']
