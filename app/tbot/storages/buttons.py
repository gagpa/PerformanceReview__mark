"""
Файл с кнопками для клавиатур.
"""

from app.tbot.extensions import ButtonTemplate

BUTTONS_TEMPLATES = \
    {
        'review_form_send_to_boss': ButtonTemplate('review_form_send_to_boss', 'Отправить руководителю 📨'),
        'review_form_achievements_list': ButtonTemplate('review_form_achievements_list', 'Достижения'),
        'review_form_back_achievements': ButtonTemplate('review_form_fails', '« К достижениям'),
        'review_form_achievements_add': ButtonTemplate('review_form_achievements_add', 'Добавить'),
        'review_form_achievement_delete': ButtonTemplate('review_form_achievement_delete'),
        'review_form_achievement_edit': ButtonTemplate('review_form_achievement_edit'),
        'review_form_achievements_delete_choose': ButtonTemplate('review_form_achievements_delete_choose', 'Удалить'),
        'review_form_achievements_edit_choose': ButtonTemplate('review_form_achievements_edit_choose', 'Изменить'),
        'review_send_coworkers': ButtonTemplate('boss_review_accept', 'Отправить коллегам 📨'),

        'boss_review_accept': ButtonTemplate('boss_review_accept', 'Принять'),
        'boss_review_decline': ButtonTemplate('boss_review_decline', 'На доработку'),
        'boss_review_form': ButtonTemplate('boss_review_form'),
        'boss_review_list': ButtonTemplate('boss_review_list', '« К списку'),
        'boss_review_update_list': ButtonTemplate('boss_review_list', '↻'),
        'boss_review_sort_asc': ButtonTemplate('boss_review_list', '🔺').add(asc=True),
        'boss_review_sort_desc': ButtonTemplate('boss_review_list', '🔻').add(asc=False),
        'boss_review_to_form': ButtonTemplate('boss_review_form', 'Посмотреть анкету'),
        'boss_review_to_list': ButtonTemplate('boss_review_list', 'Список анкет'),

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
        'coworkers_review_to_form': ButtonTemplate('coworker_review_form', 'Анкета коллеги'),
        'coworkers_review_to_list': ButtonTemplate('coworker_review_list', 'Список'),

        'review_form_fails': ButtonTemplate('review_form_fails', 'Провалы'),
        'review_form_back_fails': ButtonTemplate('review_form_fails', '« К провалам'),
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
        'review_form_back_projects': ButtonTemplate('review_form_projects_list', '« К проектам'),
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
        'hr_review_sort_desc': ButtonTemplate('hr_review_list', '🔻').add(asc=False),
        'hr_review_to_form': ButtonTemplate('hr_review_form', 'Анкета с оценками'),
        'hr_review_to_list': ButtonTemplate('hr_review_list', 'Список'),
        'get_position': ButtonTemplate('get_position'),
        'get_department': ButtonTemplate('get_department'),

        'request_view': ButtonTemplate('request_view'),
        'request_delete_view': ButtonTemplate('request_delete_view', 'Удалить'),
        'request_accept_view': ButtonTemplate('request_accept_view', 'Принять'),
        'request_view_back': ButtonTemplate('request_view_back', 'Назад'),
        'request_delete': ButtonTemplate('request_delete', 'Удалить'),
        'cancel_deletion': ButtonTemplate('cancel_deletion', 'Отмена'),

        'user_view': ButtonTemplate('user_view'),
        'user_delete_view': ButtonTemplate('user_delete_view', 'Удалить'),
        'user_view_back': ButtonTemplate('user_view_back', 'Назад'),
        'user_edit_view': ButtonTemplate('user_edit_view', 'Редактировать'),
        'user_delete': ButtonTemplate('user_delete', 'Удалить'),
        'cancel_user_delete': ButtonTemplate('cancel_user_delete', 'Отмена'),

        'user_edit_fullname': ButtonTemplate('user_edit_fullname', 'ФИО'),
        'user_edit_role': ButtonTemplate('user_edit_role', 'Роль'),
        'user_edit_position': ButtonTemplate('user_edit_position', 'Должность'),
        'user_edit_boss': ButtonTemplate('user_edit_boss', 'Руководитель'),
        'user_edit_department': ButtonTemplate('user_edit_department', 'Отдел'),

        'review_period_start': ButtonTemplate('review_period_start', 'Запуск'),
        'review_period_stop': ButtonTemplate('review_period_stop', 'Остановка'),

        'get_rapport': ButtonTemplate('get_rapport'),
        'get_hr_rapport': ButtonTemplate('get_hr_rapport', 'Для HR'),
        'get_boss_rapport': ButtonTemplate('get_boss_rapport', 'Для руководителя'),
        'employee_review': ButtonTemplate('employee_review'),
        'input_summary': ButtonTemplate('input_summary', 'Ввести summaries'),
        'change_summary': ButtonTemplate('input_summary', 'Изменить summaries'),
        'get_current_rapport': ButtonTemplate('get_current_rapport', 'Выгрузить анкету'),
        'current_forms_list': ButtonTemplate('current_forms_list', 'Назад'),

    }

__all__ = ['BUTTONS_TEMPLATES']
