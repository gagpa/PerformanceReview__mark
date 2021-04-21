"""
Файл с командами.
"""
from app.tbot.resources.review_period_views.archive_views import old_forms_list
from app.tbot.resources.boss_review_views import boss_review_list_forms_view
from app.tbot.resources.coworker_review_views import coworker_review_list_forms_view
from app.tbot.resources.request_views import request_list_view
from app.tbot.resources.review_form_views import review_form_view
from app.tbot.resources.hr_review_views import hr_review_list_forms_view
from app.tbot.resources.review_period_views.current_review_views import current_forms_list
from app.tbot.resources.review_period_views.review_period_views import review_period
from app.tbot.resources.user_views.users_list_views import users_list_view
from app.tbot.resources.registrations_views import start_auth

COMMANDS = \
    {
        'start': start_auth,
        'form': review_form_view,
        'boss': boss_review_list_forms_view,
        'coworker': coworker_review_list_forms_view,
        'hr': hr_review_list_forms_view,

        'Запросы': request_list_view,
        'Пользователи': users_list_view,
        'Запуск Review': review_period,
        'Архив': old_forms_list,
        'Текущий Review': current_forms_list,

    }

__all__ = ['COMMANDS']