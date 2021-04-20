import telebot_calendar

from app.tbot import bot
from app.tbot.resources.review_period_views.review_period_views import first_date_period, \
    second_date_period


def calendar_handler(request):
    call = request.args['call']
    call_data, action, year, month, day = call.data.split(':')
    # Обработка календаря. Получить дату или None, если кнопки другого типа
    date = telebot_calendar.calendar_query_handler(
        bot=bot, call=call, name=call_data, action=action, year=year, month=month, day=day
    )
    if action == "DAY":
        if call_data == 'first_date_period':
            return first_date_period(request, date)
        elif 'date_period_2' in call_data:
            return second_date_period(request, date)
    elif action == "CANCEL":
        return 'Календарь закрыт'
