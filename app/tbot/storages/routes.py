"""
Файл с маршрутами.
"""
from app.tbot.resources.boss_review_views import \
    boss_review_form_view, \
    boss_review_list_forms_view, \
    boss_review_decline_form_view, \
    boss_review_accept_form_view

from app.tbot.resources.coworker_review_views import \
    coworker_review_projects_view, \
    coworker_review_list_forms_view, \
    coworker_review_project_view, \
    coworker_review_form_view, \
    coworker_review_form_send_to_hr, \
    coworker_review_project_rate_choose_view, \
    coworker_review_project_rate_view, \
    coworker_review_advice_todo_view, \
    coworker_review_project_comment_on_view, \
    coworker_review_advice_not_todo_view

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
    review_form_achievement_edit_view,\
    review_form_achievements_edit_choose_view, \
    review_form_achievement_delete_view,\
    review_form_achievements_delete_choose_view

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
        'coworker_review_projects': coworker_review_projects_view,
        'coworker_review_project': coworker_review_project_view,
        'coworker_review_project_rate_choose': coworker_review_project_rate_choose_view,
        'coworker_review_project_rate': coworker_review_project_rate_view,
        'coworker_review_todo': coworker_review_advice_todo_view,
        'coworker_review_not_todo': coworker_review_advice_not_todo_view,
        'coworker_review_project_comment_on': coworker_review_project_comment_on_view,
    }

__all__ = ['ROUTES']
