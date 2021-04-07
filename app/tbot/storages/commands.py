"""
Файл с командами.
"""
from app.tbot.resources.boss_review_views import boss_review_list_forms_view
from app.tbot.resources.coworker_review_views import coworker_review_list_forms_view
from app.tbot.resources.review_form_views import review_form_view

COMMANDS = \
    {
        'start': '',
        'form': review_form_view,
        'boss_review': boss_review_list_forms_view,
        'coworker_review': coworker_review_list_forms_view,

    }

__all__ = ['COMMANDS']
