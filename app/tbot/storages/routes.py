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
    coworker_review_advices_add_view, \
    coworker_review_advices_delete_choose_view, \
    coworker_review_advices_edit_choose_view, \
    coworker_review_delete_view, \
    coworker_review_edit_view, \
    coworker_review_advices_list_view, \
    coworker_review_project_save_comment_view, \
    coworker_review_project_choose_rate_view

from app.tbot.resources.hr_review_views import \
    hr_review_list_forms_view, \
    hr_review_form_view, \
    hr_review_accept_view, \
    hr_review_decline_view, \
    hr_review_todo_view, \
    hr_review_ratings_view, \
    hr_review_comment_rating_view, \
    hr_review_send_back_view, \
    hr_comment_advice_view
from app.tbot.resources.registrations_views.auth_views import add_position_user, \
    add_department_user, add_new_username

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
    review_form_duties_add_view, \
    review_form_duties_list_view, \
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
    review_form_project_contacts_view, \
    review_form_project_edit_description_view, \
    review_form_project_edit_name_view, \
    review_form_projects_delete_choose_view, \
    review_form_projects_edit_choose_view, \
    review_form_send_to_boss_view, \
    review_form_achievement_edit_view, \
    review_form_achievements_edit_choose_view, \
    review_form_achievement_delete_view, \
    review_form_achievements_delete_choose_view, \
    copy_last_review, \
    review_form_achievements_delete_choose_view, \
    review_form_duties_edit_choose_view, \
    review_form_duties_delete_choose_view, \
    review_form_duty_edit_view, \
    review_form_duty_delete_view, \
    review_form_project_delete_contact_view, \
    review_form_project_delete_choose_contact_view, \
    review_form_add_contact_in_current_project_view, \
    review_form_project_edit_choose_contact_view, \
    review_form_project_change_contact_view, \
    review_form_project_add_description_view, \
review_form_project_choose_department

from app.tbot.resources.review_period_views.archive_views import old_forms_list, old_review_list

from app.tbot.resources.review_period_views.current_review_views import employee_review, \
    current_forms_list, input_summary
from app.tbot.resources.review_period_views.rapport_views import get_rapport, get_hr_rapport, \
    get_boss_rapport, send_rapport_to_boss

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
    users_list_view, \
    choose_departments_view
from app.tbot.resources import only_on_review

ROUTES = \
    {
        'form': only_on_review(review_form_view),
        'duties': only_on_review(review_form_duties_list_view),
        'duties_add': only_on_review(review_form_duties_add_view),
        'duties_edit_choose': only_on_review(review_form_duties_edit_choose_view),
        'duty_edit': only_on_review(review_form_duty_edit_view),
        'duty_delete': only_on_review(review_form_duty_delete_view),
        'duties_delete_choose': only_on_review(review_form_duties_delete_choose_view),
        'project_add': only_on_review(review_form_project_add_view),
        'con_add': only_on_review(review_form_project_add_description_view),
        'con_dep': only_on_review(review_form_project_choose_department),
        'project_delete': only_on_review(review_form_project_delete_view),
        'project_delete_choose': only_on_review(review_form_projects_delete_choose_view),
        'projects': only_on_review(review_form_projects_list_view),
        'project_edit_choose': only_on_review(review_form_projects_edit_choose_view),
        'project_edit': only_on_review(review_form_project_edit_view),
        'project_edit_name': only_on_review(review_form_project_edit_name_view),
        'project_edit_description': only_on_review(review_form_project_edit_description_view),
        'project_contacts': only_on_review(review_form_project_contacts_view),
        'project_delete_contact': only_on_review(review_form_project_delete_contact_view),
        'project_edit_choose_contact': only_on_review(review_form_project_edit_choose_contact_view),
        'add_contact_in_current_project': only_on_review(review_form_add_contact_in_current_project_view),
        'project_change_contact': only_on_review(review_form_project_change_contact_view),
        'achievements': only_on_review(review_form_achievements_list_view),
        'achievements_add': only_on_review(review_form_achievements_add_view),
        'achievements_edit_choose': only_on_review(review_form_achievements_edit_choose_view),
        'achievement_edit': only_on_review(review_form_achievement_edit_view),
        'achievement_delete': only_on_review(review_form_achievement_delete_view),
        'achievements_delete_choose': only_on_review(review_form_achievements_delete_choose_view),
        'fails': only_on_review(review_form_fails_list_view),
        'fail_delete': only_on_review(review_form_fail_delete_view),
        'fails_add': only_on_review(review_form_fails_add_view),
        'fail_edit': only_on_review(review_form_fail_edit_view),
        'fails_edit_choose': only_on_review(review_form_fails_edit_choose_view),
        'fails_delete_choose': only_on_review(review_form_fails_delete_choose_view),
        'form_send_to_boss': only_on_review(review_form_send_to_boss_view),
        'project_delete_choose_contact': only_on_review(review_form_project_delete_choose_contact_view),
        'boss_review_list': only_on_review(boss_review_list_forms_view),
        'boss_form': only_on_review(boss_review_form_view),
        'boss_accept': only_on_review(boss_review_accept_form_view),
        'boss_decline': only_on_review(boss_review_decline_form_view),
        'form_send_to_hr': only_on_review(coworker_review_form_send_to_hr),
        'coworker_form': only_on_review(coworker_review_form_view),
        'coworker_review_list': only_on_review(coworker_review_list_forms_view),
        'coworker_projects': only_on_review(coworker_review_projects_view),
        'coworker_project': only_on_review(coworker_review_project_view),
        'coworker_rate': only_on_review(coworker_review_project_rate_view),
        'coworker_choose_rate': only_on_review(coworker_review_project_choose_rate_view),

        'coworker_comment': only_on_review(coworker_review_project_comment_view),

        'advices': only_on_review(coworker_review_advices_list_view),
        'advices_add': only_on_review(coworker_review_advices_add_view),
        'advices_delete': only_on_review(coworker_review_delete_view),
        'advices_edit': only_on_review(coworker_review_edit_view),
        'advices_delete_choose': only_on_review(coworker_review_advices_delete_choose_view),
        'advices_edit_choose': only_on_review(coworker_review_advices_edit_choose_view),

        'hr_review_list': only_on_review(hr_review_list_forms_view),
        'hr_form': only_on_review(hr_review_form_view),
        'hr_review_accept': only_on_review(hr_review_accept_view),
        'hr_review_decline': only_on_review(hr_review_decline_view),
        'hr_todo': only_on_review(hr_review_todo_view),
        'hr_ratings': only_on_review(hr_review_ratings_view),
        'hr_comment_rating': only_on_review(hr_review_comment_rating_view),
        'hr_send_back': only_on_review(hr_review_send_back_view),
        'hr_advices_edit': only_on_review(hr_comment_advice_view),
        'get_position': add_department_user,
        'get_department': add_position_user,
        'get_reg': add_new_username,
        'request_view': request_view,
        'request_list_view': request_list_view,
        'request_delete_view': delete_request_view,
        'request_view_back': request_list_view,
        'request_accept_view': accept_request_view,
        'request_delete': delete_request,
        'cancel_deletion': request_list_view,
        'to_request': request_view,

        'user_view': user_view,
        'user_list_view': users_list_view,
        'user_delete_view': delete_user_view,
        'user_view_back': users_list_view,
        'choose_dep': choose_departments_view,
        'user_edit_view': edit_user_view,
        'user_delete': delete_user,
        'cancel_user_delete': users_list_view,
        'edit_position': change_user_position,
        'edit_department': change_user_department,
        'edit_role': change_user_role,
        'back_to_user': user_view,

        'edit_fullname': user_edit_fullname,
        'user_edit_role': user_edit_role,
        'user_edit_position': user_edit_position,
        'user_edit_boss': user_edit_boss,
        'user_edit_department': user_edit_department,
        'back_to_edit': edit_user_view,

        'review_period_start': review_period_start,
        'review_period_stop': review_period_stop,
        'first_date_period': calendar_handler,
        'date_period_2': calendar_handler,
        'copy_last_form': copy_last_review,

        'forms_list': current_forms_list,
        'get_old_review': old_forms_list,
        'old_review_list': old_review_list,
        'back_to_old_review_list': old_review_list,
        'get_rapport': get_rapport,
        'back_to_rapport': old_forms_list,
        'back_to_form': employee_review,
        'get_hr_rapport': get_hr_rapport,
        'get_boss_rapport': get_boss_rapport,
        'send_rap_to_boss': send_rapport_to_boss,
        'employee_review': employee_review,
        'current_forms_list': current_forms_list,
        'input_summary': input_summary,
        'change_summary': input_summary,
        'get_current_rapport': get_rapport,
    }

__all__ = ['ROUTES']
