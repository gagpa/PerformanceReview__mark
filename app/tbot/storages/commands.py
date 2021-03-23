"""
Файл с командами.
"""
from app.tbot.resources.boss_review_views import controller_boss_review_list
from app.tbot.resources.review_form_views import controller_form

COMMANDS = \
    {
        'start': '',
        'form': controller_form,
        'boss_review': controller_boss_review_list,

    }


__all__ = ['COMMANDS']
