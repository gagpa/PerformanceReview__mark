"""
Файл с маршрутами.
"""
from app.tbot.resources.boss_review_views import \
    boss_review_form_view, \
    boss_review_list_forms_view, \
    boss_review_decline_form_view, \
    boss_review_accept_form_view

from app.tbot.resources.calendar_views import calendar_handler

from app.tbot.resources.coworker_review_views import \
    coworker_review_projects_view, \
    coworker_review_list_forms_view, \
    coworker_review_project_view, \
    coworker_review_form_view, \
    coworker_review_form_send_to_hr, \
    coworker_review_project_comment_view, \
    coworker_review_project_rate_view, \
    coworker_review_advice_todo_view, \
    coworker_review_advice_not_todo_view

from app.tbot.resources.hr_review_views import \
    hr_review_list_forms_view, \
    hr_review_form_view, \
    hr_review_accept_view, \
    hr_review_decline_view, \
    hr_review_todo_view, \
    hr_review_ratings_view, \
    hr_review_comment_rating_view, \
    hr_review_send_back_view
from app.tbot.resources.registrations_views.auth_views import add_position_user, \
    add_department_user

from app.tbot.resources.request_views import \
    request_view, \
    request_list_view

from app.tbot.resources.request_views.request_view import \
    delete_request_view, \
    accept_request_view, delete_request

from app.tbot.resources.review_form_views import \
    review_form_view, \
    review_form_achievements_add_view, \
    review_form_achievements_list_view, \
    review_form_duty_add_view, \
    review_form_duty_edit_view, \
    review_form_duty_list_view, \
    review_form_fail_delete_view, \
    review_form_fails_add_view, \
    review_form_fails_list_view, \
    review_form_fail_edit_view, \
    review_form_project_add_view, \
    review_form_project_delete_view, \
    review_form_project_edit_view, \
    review_form_projects_list_view, \
    review_form_fails_delete_choose_view, \
    review_form_fails_edit_choose_view, \
    review_form_project_edit_contacts_view, \
    review_form_project_edit_description_view, \
    review_form_project_edit_name_view, \
    review_form_projects_delete_choose_view, \
    review_form_projects_edit_choose_view, \
    review_form_send_to_boss_view, \
    review_form_achievement_edit_view, \
    review_form_achievements_edit_choose_view, \
    review_form_achievement_delete_view, \
    review_form_achievements_delete_choose_view
from app.tbot.resources.review_period_views.archive_views import old_forms_list, old_review_list

from app.tbot.resources.review_period_views.current_review_views import employee_review, \
    current_forms_list, input_summary
from app.tbot.resources.review_period_views.rapport_views import get_rapport, get_hr_rapport, \
    get_boss_rapport

from app.tbot.resources.review_period_views.review_period_views import \
    review_period_start, \
    review_period_stop

from app.tbot.resources.user_views.user_views import \
    delete_user_view, \
    edit_user_view, \
    user_edit_fullname, \
    user_edit_role, \
    user_edit_position, \
    user_edit_boss, \
    user_edit_department, delete_user, change_user_position, change_user_department, \
    change_user_role

from app.tbot.resources.user_views.users_list_views import \
    user_view, \
    users_list_view

ROUTES = \
    {
        'review_form': review_form_view,
        'review_form_duty': review_form_duty_list_view,
        'review_form_duty_add': review_form_duty_add_view,
        'review_form_duty_edit': review_form_duty_edit_view,
        'review_form_project_add': review_form_project_add_view,
        'review_form_project_delete': review_form_project_delete_view,
        'review_form_project_delete_choose': review_form_projects_delete_choose_view,
        'review_form_projects_list': review_form_projects_list_view,
        'review_form_project_edit_choose': review_form_projects_edit_choose_view,
        'review_form_project_edit': review_form_project_edit_view,
        'review_form_project_edit_name': review_form_project_edit_name_view,
        'review_form_project_edit_description': review_form_project_edit_description_view,
        'review_form_project_edit_contacts': review_form_project_edit_contacts_view,

        'review_form_achievements_list': review_form_achievements_list_view,
        'review_form_achievements_add': review_form_achievements_add_view,
        'review_form_achievements_edit_choose': review_form_achievements_edit_choose_view,
        'review_form_achievement_edit': review_form_achievement_edit_view,
        'review_form_achievement_delete': review_form_achievement_delete_view,
        'review_form_achievements_delete_choose': review_form_achievements_delete_choose_view,

        'review_form_fails': review_form_fails_list_view,
        'review_form_fail_delete': review_form_fail_delete_view,
        'review_form_fails_add': review_form_fails_add_view,
        'review_form_fail_edit': review_form_fail_edit_view,
        'review_form_fails_edit_choose': review_form_fails_edit_choose_view,
        'review_form_fails_delete_choose': review_form_fails_delete_choose_view,
        'review_form_send_to_boss': review_form_send_to_boss_view,

        'boss_review_list': boss_review_list_forms_view,
        'boss_review_form': boss_review_form_view,
        'boss_review_accept': boss_review_accept_form_view,
        'boss_review_decline': boss_review_decline_form_view,
        'coworker_review_form_send_to_hr': coworker_review_form_send_to_hr,
        'coworker_review_form': coworker_review_form_view,
        'coworker_review_list': coworker_review_list_forms_view,
        'coworker_projects': coworker_review_projects_view,
        'coworker_project': coworker_review_project_view,
        'coworker_rate': coworker_review_project_rate_view,
        'coworker_review_todo': coworker_review_advice_todo_view,
        'coworker_review_not_todo': coworker_review_advice_not_todo_view,
        'coworker_comment': coworker_review_project_comment_view,

        'hr_review_list': hr_review_list_forms_view,
        'hr_review_form': hr_review_form_view,
        'hr_review_accept': hr_review_accept_view,
        'hr_review_decline': hr_review_decline_view,
        'hr_review_todo': hr_review_todo_view,
        'hr_review_ratings': hr_review_ratings_view,
        'hr_review_comment_rating': hr_review_comment_rating_view,
        'hr_review_send_back': hr_review_send_back_view,

        'get_position': add_position_user,
        'get_department': add_department_user,

        'request_view': request_view,
        'request_delete_view': delete_request_view,
        'request_view_back': request_list_view,
        'request_accept_view': accept_request_view,
        'request_delete': delete_request,
        'cancel_deletion': request_list_view,
        'to_request': request_view,

        'user_view': user_view,
        'user_delete_view': delete_user_view,
        'user_view_back': users_list_view,
        'user_edit_view': edit_user_view,
        'user_delete': delete_user,
        'cancel_user_delete': users_list_view,
        'edit_position': change_user_position,
        'edit_department': change_user_department,
        'edit_role': change_user_role,
        'back_to_user': user_view,

        'user_edit_fullname': user_edit_fullname,
        'user_edit_role': user_edit_role,
        'user_edit_position': user_edit_position,
        'user_edit_boss': user_edit_boss,
        'user_edit_department': user_edit_department,

        'review_period_start': review_period_start,
        'review_period_stop': review_period_stop,
        'first_date_period': calendar_handler,
        'date_period_2': calendar_handler,

        'forms_list': current_forms_list,
        'get_old_review': old_forms_list,
        'old_review_list': old_review_list,
        'back_to_old_review_list': old_review_list,
        'get_rapport': get_rapport,
        'back_to_rapport': old_forms_list,
        'get_hr_rapport': get_hr_rapport,
        'get_boss_rapport': get_boss_rapport,
        'employee_review': employee_review,
        'current_forms_list': current_forms_list,
        'input_summary': input_summary,
        'change_summary': input_summary,
        'get_current_rapport': get_rapport,
    }

__all__ = ['ROUTES']
