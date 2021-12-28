import datetime

from app.db import Session
from app.models import ReviewPeriod, User, Role, Form
from app.services.review import ReviewPeriodService
from app.tbot import notificator
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
    users = Session().query(User).join(Role, User.role) \
        .filter(Role.name != 'Undefined').all()
    notificator.notificate(Notification(view='start_review', review=service.current,
                                        date=second_date.strftime('%d-%m-%Y')),
                           *[user.chat_id for user in users])
    check_last_form(users)
    return ReviewPeriodForm(started=True)


def check_last_form(users):
    """ Посмотреть есть ли анкета в предыдущем ревью """
    for user in users:
        last_form = Session().query(Form) \
            .filter_by(user_id=user.id) \
            .order_by(Form.created_at.desc()).first()
        if last_form:
            notificator.notificate(Notification(view='copy_last_form',
                                                review=ReviewPeriodService().current,
                                                last_form=last_form),
                                   user.chat_id)


def review_period_stop(request):
    service = ReviewPeriodService()
    review = service.by(is_active=True)
    if service:
        review.is_active = False
        review.end_date = datetime.datetime.now()
    Session.commit()
    service.send_to_archive()
    return ReviewPeriodForm(stopped=True)
