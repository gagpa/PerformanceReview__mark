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
        'boss_review_list': ButtonTemplate('Список', 'boss_review_list'),

        'coworker_review_form': ButtonTemplate('coworker_review_form', 'Анкета'),
        'coworker_review_list': ButtonTemplate('coworker_review_list', 'Список'),
        'coworker_review_projects': ButtonTemplate('coworker_review_projects', 'Оценить проекты'),
        'coworker_review_projects_choose': ButtonTemplate('coworker_review_project'),
        'coworker_review_project_choose_rate': ButtonTemplate('coworker_review_project_rate'),
        'coworker_review_project_rate': ButtonTemplate('coworker_review_project_rate', 'Оценить'),
        'coworker_review_todo': ButtonTemplate('coworker_review_todo', 'Что делать'),
        'coworker_review_not_todo': ButtonTemplate('coworker_review_not_todo', 'Что не делать'),
        'coworker_review_form_send_to_hr': ButtonTemplate('coworker_review_form_send_to_hr', 'Отправить HR'),

        'review_form_fails': ButtonTemplate('review_form_fails', 'Провалы'),
        'review_form_fails_add': ButtonTemplate('review_form_fails_add', 'Добавить'),
        'review_form_fail_delete': ButtonTemplate('review_form_fail_delete'),
        'review_form_fail_edit': ButtonTemplate('review_form_fail_edit'),
        'review_form_fails_delete_choose': ButtonTemplate('review_form_fails_delete_choose', 'Удалить'),
        'review_form_fails_edit_choose': ButtonTemplate('review_form_fails_edit_choose', 'Изменить'),

        'review_form': ButtonTemplate('review_form', 'Анкета'),

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

        'request_view': ButtonTemplate('request_view'),
        'request_delete_view': ButtonTemplate('request_delete_view', 'Удалить'),
        'request_accept_view': ButtonTemplate('request_accept_view', 'Принять'),
        'request_view_back': ButtonTemplate('request_view_back', 'Назад'),

        'user_view': ButtonTemplate('user_view'),
        'user_delete_view': ButtonTemplate('user_delete_view', 'Удалить'),
        'user_view_back': ButtonTemplate('user_view_back', 'Назад'),
        'user_edit_view': ButtonTemplate('user_edit_view', 'Редактировать'),

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
    }

__all__ = ['BUTTONS_TEMPLATES']
