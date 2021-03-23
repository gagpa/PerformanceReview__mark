"""
Файл с маршрутами.
"""
from app.tbot.resources.boss_review_views import \
    controller_boss_review_list, \
    controller_boss_review_form, \
    controller_boss_review_accept, \
    controller_boss_review_decline

from app.tbot.resources.coworker_review_views import \
    controller_coworker_review_list, \
    controller_coworker_review_form

from app.tbot.resources.review_form_views import \
    controller_form, \
    controller_duty, \
    controller_duty_add, \
    controller_duty_edit, \
    controller_project_add, \
    controller_project_delete, \
    controller_projects, \
    controller_project_edit_choose, \
    controller_project_delete_choose, \
    controller_project_edit, \
    controller_project_edit_name, \
    controller_project_edit_description, \
    controller_project_edit_contacts, \
    controller_achievements, \
    controller_achievements_add, \
    controller_achievements_edit_choose, \
    controller_achievement_edit, \
    controller_achievement_delete, \
    controller_achievements_delete_choose, \
    controller_fails, \
    controller_fail_delete, \
    controller_fails_add, \
    controller_fail_edit, \
    controller_fails_edit_choose, \
    controller_fails_delete_choose, \
    controller_send_to_boss

ROUTES = \
    {
        'form': controller_form,
        'duty': controller_duty,
        'duty_add': controller_duty_add,
        'duty_edit': controller_duty_edit,
        'project_add': controller_project_add,
        'project_delete': controller_project_delete,
        'projects': controller_projects,
        'project_edit_choose': controller_project_edit_choose,
        'project_delete_choose': controller_project_delete_choose,
        'project_edit': controller_project_edit,
        'project_edit_name': controller_project_edit_name,
        'project_edit_description': controller_project_edit_description,
        'project_edit_contacts': controller_project_edit_contacts,

        'achievements': controller_achievements,
        'achievements_add': controller_achievements_add,
        'achievements_edit_choose': controller_achievements_edit_choose,
        'achievement_edit': controller_achievement_edit,
        'achievement_delete': controller_achievement_delete,
        'achievements_delete_choose': controller_achievements_delete_choose,

        'fails': controller_fails,
        'fail_delete': controller_fail_delete,
        'fails_add': controller_fails_add,
        'fail_edit': controller_fail_edit,
        'fails_edit_choose': controller_fails_edit_choose,
        'fails_delete_choose': controller_fails_delete_choose,
        'send_to_boss': controller_send_to_boss,

        'boss_review_list': controller_boss_review_list,
        'boss_review_form': controller_boss_review_form,
        'boss_review_accept': controller_boss_review_accept,
        'boss_review_decline': controller_boss_review_decline,

        'coworker_review_form': controller_coworker_review_form,
        'coworker_review_list': controller_coworker_review_list,
        # 'coworker_review_projects'
        # 'coworker_review_todo'
        # 'coworker_review_not_todo'
        # 'coworker_review_send_to_hr'
    }

__all__ = ['ROUTES']
