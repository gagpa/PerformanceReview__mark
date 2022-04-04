"""
Файл с кнопками для клавиатур.
"""

from copy import deepcopy

from app.tbot.extensions import ButtonTemplate

TEMPLATES = \
    {
        'review_form_send_to_boss': ButtonTemplate('form_send_to_boss', 'Отправить руководителю 📨'),
        'review_form_achievements_list': ButtonTemplate('achievements', 'Достижения'),
        'review_form_back_achievements': ButtonTemplate('achievements', '« К достижениям'),
        'review_form_achievements_add': ButtonTemplate('achievements_add', 'Добавить'),
        'review_form_achievement_delete': ButtonTemplate('achievement_delete'),
        'review_form_achievement_edit': ButtonTemplate('achievement_edit'),
        'review_form_achievements_delete_choose': ButtonTemplate('achievements_delete_choose', 'Удалить'),
        'review_form_achievements_edit_choose': ButtonTemplate('achievements_edit_choose', 'Изменить'),
        'review_send_coworkers': ButtonTemplate('boss_accept', 'Отправить коллегам 📨'),
        'review_form_fails': ButtonTemplate('fails', 'Провалы'),
        'review_form_back_fails': ButtonTemplate('fails', '« К провалам'),
        'review_form_fails_add': ButtonTemplate('fails_add', 'Добавить'),
        'review_form_fail_delete': ButtonTemplate('fail_delete'),
        'review_form_fail_edit': ButtonTemplate('fail_edit'),
        'review_form_fails_delete_choose': ButtonTemplate('fails_delete_choose', 'Удалить'),
        'review_form_fails_edit_choose': ButtonTemplate('fails_edit_choose', 'Изменить'),
        'review_form': ButtonTemplate('form', '« К анкете'),
        'review_to_form': ButtonTemplate('form', 'Анкета'),
        'review_form_duties_list': ButtonTemplate('duties', 'Обязанности'),
        'review_form_back_duties': ButtonTemplate('duties', '« К обязанностям'),
        'review_form_duties_add': ButtonTemplate('duties_add', 'Добавить'),
        'review_form_duty_delete': ButtonTemplate('duty_delete'),
        'review_form_duty_edit': ButtonTemplate('duty_edit'),
        'review_form_duties_delete_choose': ButtonTemplate('duties_delete_choose', 'Удалить'),
        'review_form_duties_edit_choose': ButtonTemplate('duties_edit_choose', 'Изменить'),
        'review_form_project_delete_contact': ButtonTemplate('project_delete_contact'),
        'review_form_projects_list': ButtonTemplate('projects', 'Проекты'),
        'review_form_back_projects': ButtonTemplate('projects', '« К проектам'),
        'review_form_project_add': ButtonTemplate('project_add', 'Добавить проект'),
        'review_form_project_contacts_on_create': ButtonTemplate('con_add', 'Оценивающие'),
        'review_form_project_contacts_on_create_dep': ButtonTemplate('con_dep', 'Другие отделы'),
        'review_form_project_contacts_on_create_done': ButtonTemplate('projects', 'Следующий шаг'),
        'review_form_project_delete': ButtonTemplate('project_delete'),
        'review_form_project_edit': ButtonTemplate('project_edit'),
        'review_form_project_edit_name': ButtonTemplate('project_edit_name', 'Название'),
        'review_form_project_edit_description': ButtonTemplate('project_edit_description', 'Роль и результаты'),
        'review_form_project_delete_choose': ButtonTemplate('project_delete_choose', 'Удалить проект'),
        'review_form_project_edit_choose': ButtonTemplate('project_edit_choose', 'Изменить проект'),
        'review_form_back_projects_list': ButtonTemplate('projects', '« К Проектам'),
        'review_form_projects_examples': ButtonTemplate('projects', 'Пример').add(example=True),
        'review_form_projects_descriptions': ButtonTemplate('projects', '« К описанию'),
        'review_form_project_contacts': ButtonTemplate('project_contacts', 'Оценивающие'),
        'review_form_project_add_contact': ButtonTemplate('project_add_contact', 'Добавить'),
        'review_form_project_delete_choose_contact': ButtonTemplate('project_delete_choose_contact',
                                                                    'Удалить'),
        'review_form_project_edit_choose_contact': ButtonTemplate('project_edit_choose_contact',
                                                                  'Изменить'),
        'review_form_add_contact_in_current_project': ButtonTemplate('add_contact_in_current_project',
                                                                     'Добавить'),
        'review_form_project_edit_contact': ButtonTemplate('project_change_contact'),
        'review_form_project_contacts_back': ButtonTemplate('project_contacts', '« Назад'),
        'review_form_project_edit_back': ButtonTemplate('project_edit', '« Назад'),

        'boss_review_accept': ButtonTemplate('boss_accept', 'Принять'),
        'boss_review_decline': ButtonTemplate('boss_decline', 'На доработку'),
        'boss_review_form': ButtonTemplate('boss_form'),
        'boss_review_list': ButtonTemplate('boss_review_list', '« К списку'),
        'boss_review_update_list': ButtonTemplate('boss_review_list', 'Обновить список'),
        'boss_review_sort_asc': ButtonTemplate('boss_review_list', '🔺').add(asc=True),
        'boss_review_sort_desc': ButtonTemplate('boss_review_list', '🔻').add(asc=False),
        'boss_review_to_form': ButtonTemplate('boss_form', 'Посмотреть анкету'),
        'boss_review_to_list': ButtonTemplate('boss_review_list', 'Список анкет'),

        'coworker_review_form': ButtonTemplate('coworker_form', 'Анкета'),
        'coworker_review_list': ButtonTemplate('coworker_review_list', '« К анкете'),
        'coworker_projects': ButtonTemplate('coworker_projects', 'Оценить проекты'),
        'coworker_project': ButtonTemplate('coworker_project'),
        'coworker_rate': ButtonTemplate('coworker_rate', 'Оценить'),
        'coworker_back_form': ButtonTemplate('coworker_form', '« К анкете'),
        'coworker_back_projects': ButtonTemplate('coworker_projects', '« К проектам'),
        'coworker_comment': ButtonTemplate('coworker_comment', 'Изменить комментарий'),
        'coworker_review_todo': ButtonTemplate('coworker_review_todo', 'Что делать'),
        'coworker_review_not_todo': ButtonTemplate('coworker_review_not_todo', 'Что перестать делать'),
        'coworker_review_form_send_to_hr': ButtonTemplate('form_send_to_hr', 'Отправить HR'),
        'coworker_review_sort_asc': ButtonTemplate('coworker_review_list', '🔺').add(asc=True),
        'coworker_review_sort_desc': ButtonTemplate('coworker_review_list', '🔻').add(asc=False),
        'coworker_review_update_list': ButtonTemplate('coworker_review_list', 'Обновить список'),
        'coworkers_review_to_form': ButtonTemplate('coworker_form', 'Анкета коллеги'),
        'coworkers_review_to_list': ButtonTemplate('coworker_review_list', 'Список анкет на проверку'),
        'coworker_review_advices': ButtonTemplate('advices', 'Советы'),
        'coworker_review_advices_todo': ButtonTemplate('advices', 'Что делать?'),
        'coworker_review_advices_not_todo': ButtonTemplate('advices', 'Что перестать делать?'),
        'coworker_review_back_advices': ButtonTemplate('advices', '« К советам'),
        'coworker_review_advices_add': ButtonTemplate('advices_add', 'Добавить'),
        'coworker_review_advices_delete': ButtonTemplate('advices_delete'),
        'coworker_review_advices_edit': ButtonTemplate('advices_edit'),
        'coworker_review_advices_delete_choose': ButtonTemplate('advices_delete_choose', 'Удалить'),
        'coworker_review_advices_edit_choose': ButtonTemplate('advices_edit_choose', 'Изменить'),
        'coworker_choose_rate': ButtonTemplate('coworker_choose_rate', 'Изменить оценку'),
        'coworker_back_project': ButtonTemplate('coworker_project', '« Назад'),
        'copy_last_form': ButtonTemplate('copy_last_form', 'Скопировать предыдущую форму'),
        'review_form_duty': ButtonTemplate('duty', 'Обязанности'),
        'review_form_project_edit_contacts': ButtonTemplate('project_edit_choose_contact', 'Контакты'),

        'hr_review_list': ButtonTemplate('hr_review_list', '« К списку'),
        'hr_review_form': ButtonTemplate('hr_form'),
        'hr_review_accept': ButtonTemplate('hr_review_accept', 'Принять'),
        'hr_review_decline': ButtonTemplate('hr_review_decline', 'Отклонить'),
        'hr_review_todo': ButtonTemplate('hr_todo', 'Что начать делать'),
        'hr_review_not_todo': ButtonTemplate('hr_todo', 'Что перестать делать'),
        'hr_review_ratings': ButtonTemplate('hr_ratings', 'Оценки'),
        'hr_review_back_to_form': ButtonTemplate('hr_form', '« Назад'),
        'hr_review_back_to_form_name': ButtonTemplate('hr_form', '« К анкете'),
        'hr_review_comment_rating': ButtonTemplate('hr_comment_rating'),
        'hr_review_back_to_decline': ButtonTemplate('hr_review_decline', '« Назад'),
        'hr_review_send_back': ButtonTemplate('hr_send_back', 'Вернуть форму'),
        'hr_review_update_list': ButtonTemplate('hr_review_list', 'Обновить список'),
        'hr_review_sort_asc': ButtonTemplate('hr_review_list', '🔺').add(asc=True),
        'hr_review_sort_desc': ButtonTemplate('hr_review_list', '🔻').add(asc=False),
        'hr_review_to_form': ButtonTemplate('hr_form', 'Анкета с оценками'),
        'hr_review_to_list': ButtonTemplate('hr_review_list', 'Список анкет на проверку'),
        'hr_advices_edit': ButtonTemplate('hr_advices_edit'),

        'get_position': ButtonTemplate('get_position'),
        'get_department': ButtonTemplate('get_department'),

        'request_view': ButtonTemplate('request_view'),
        'request_list_view': ButtonTemplate('request_list_view'),
        'request_delete_view': ButtonTemplate('request_delete_view', 'Удалить'),
        'request_accept_view': ButtonTemplate('request_accept_view', 'Принять'),
        'request_view_back': ButtonTemplate('request_view_back', 'Назад'),
        'request_delete': ButtonTemplate('request_delete', 'Удалить'),
        'cancel_deletion': ButtonTemplate('cancel_deletion', 'Отмена'),
        'to_request': ButtonTemplate('to_request', 'К заявке'),

        'user_view': ButtonTemplate('user_view'),
        'user_list_view': ButtonTemplate('user_list_view'),
        'user_delete_view': ButtonTemplate('user_delete_view', 'Удалить'),
        'user_view_back': ButtonTemplate('user_view_back', 'Назад'),
        'choose_dep': ButtonTemplate('choose_dep', 'Назад'),
        'user_edit_view': ButtonTemplate('user_edit_view', 'Редактировать'),
        'user_delete': ButtonTemplate('user_delete', 'Удалить'),
        'cancel_user_delete': ButtonTemplate('cancel_user_delete', 'Отмена'),
        'back_to_user': ButtonTemplate('back_to_user', 'Назад'),

        'user_edit_fullname': ButtonTemplate('edit_fullname', 'ФИО'),
        'user_edit_role': ButtonTemplate('user_edit_role', 'Роль'),
        'user_edit_position': ButtonTemplate('user_edit_position', 'Должность'),
        'user_edit_boss': ButtonTemplate('user_edit_boss', 'Руководитель'),
        'user_edit_department': ButtonTemplate('user_edit_department', 'Отдел'),
        'edit_position': ButtonTemplate('edit_position'),
        'edit_department': ButtonTemplate('edit_department'),
        'edit_role': ButtonTemplate('edit_role'),
        'back_to_edit': ButtonTemplate('back_to_edit', 'Назад'),

        'review_period_start': ButtonTemplate('review_period_start', 'Запуск'),
        'review_period_stop': ButtonTemplate('review_period_stop', 'Остановка'),

        'forms_list': ButtonTemplate('forms_list'),
        'get_old_review': ButtonTemplate('get_old_review'),
        'old_review_list': ButtonTemplate('old_review_list'),
        'back_to_old_review_list': ButtonTemplate('back_to_old_review_list', 'Назад'),
        'get_rapport': ButtonTemplate('get_rapport'),
        'back_to_rapport': ButtonTemplate('back_to_rapport', 'Назад'),
        'back_to_form': ButtonTemplate('back_to_form', 'Назад'),
        'get_hr_rapport': ButtonTemplate('get_hr_rapport', 'Для HR'),
        'get_boss_rapport': ButtonTemplate('get_boss_rapport', 'Для руководителя'),
        'send_rapport_to_boss': ButtonTemplate('send_rap_to_boss', 'Отправить руководителю'),
        'employee_review': ButtonTemplate('employee_review'),
        'input_summary': ButtonTemplate('input_summary', 'Написать отчет'),
        'change_summary': ButtonTemplate('input_summary', 'Изменить отчет'),
        'get_current_rapport': ButtonTemplate('get_current_rapport', 'Выгрузить анкету'),
        'current_forms_list': ButtonTemplate('current_forms_list', 'Список анкет'),
        'current_forms_list_back': ButtonTemplate('current_forms_list', 'Назад'),

    }


class AdapterTemplates:

    def __getitem__(self, key):
        return deepcopy(TEMPLATES[key])


BUTTONS_TEMPLATES = AdapterTemplates()
GENERAL_BUTTONS = \
    {
        ''
    }

__all__ = ['BUTTONS_TEMPLATES']
