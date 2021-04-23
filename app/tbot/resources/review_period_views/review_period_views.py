import datetime

from loguru import logger
from telebot.apihelper import ApiTelegramException

from app.db import Session
from app.models import ReviewPeriod, User, Role
from app.services.review import ReviewPeriodService
from app.tbot import bot, notificator
from app.tbot.services.forms import Notification
from app.tbot.services.forms.review_period_form import ReviewPeriodForm


def review_period(request):
    active = Session().query(ReviewPeriod).filter_by(is_active=True).one_or_none()
    if active:
        model = ReviewPeriodService.current
        template = ReviewPeriodForm(model=model, stop=True)
    else:
        template = ReviewPeriodForm(start=True)
    return template


def review_period_start(request):
    return ReviewPeriodForm(choose_first_date_period=True)


def first_date_period(request, date):
    return ReviewPeriodForm(date=date, choose_second_date_period=True)


def second_date_period(request, date):
    first_date = request.args['first_date']
    first_date = datetime.datetime.strptime(first_date, '%d-%m-%Y')
    second_date = date
    service = ReviewPeriodService()
    service.create(is_active=True, start_date=first_date, end_date=second_date)
    Session.commit()
    users = Session().query(User).join(Role, User.role)\
        .filter(Role.name != 'Undefined').all()
    notificator.notificate(Notification(view='start_review'), *[user.chat_id for user in users])
    return ReviewPeriodForm(started=True)


def review_period_stop(request):
    service = ReviewPeriodService().by(is_active=True)
    if service:
        service.is_active = False
        service.end_date = datetime.datetime.now()
    Session.commit()
    return ReviewPeriodForm(stopped=True)
