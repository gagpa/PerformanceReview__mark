"""
Файл с командами.
"""
from app.tbot.resources.boss_review_views import controller_boss_review_list
from app.tbot.resources.coworker_review_views import controller_coworker_review_list
from app.tbot.resources.review_form_views import controller_form

COMMANDS = \
    {
        'start': '',
        'form': controller_form,
        'boss_review': controller_boss_review_list,
        'coworker_review': controller_coworker_review_list,

    }

__all__ = ['COMMANDS']
