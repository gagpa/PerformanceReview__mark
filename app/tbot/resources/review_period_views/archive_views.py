import datetime
import os

from jinja2 import FileSystemLoader, Environment
from weasyprint import HTML

from app.db import Session
from app.models import Form, ReviewPeriod, User, Rating, Status, Duty, Project, Achievement, Fail
from app.tbot import bot
from app.tbot.services.forms.archive_form import ArchiveForm


def old_forms_list(request):
    old_reviews = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Rating, Form.rating).join(Status, Form.status) \
        .filter(ReviewPeriod.is_active == False).all()
    if old_reviews:
        return ArchiveForm(models=old_reviews, archive_list=True)
    else:
        return ArchiveForm()


def get_rapport(request):
    pk = request.pk()
    return ArchiveForm(pk=pk, choose_rapport=True)


def get_hr_rapport(request):
    pk = request.args['pk'][0]
    user = request.user
    template_vars = get_data_for_rapport(pk)
    template_vars.update(reviews=[1,3,2])
    create_and_send_pdf(user.chat_id, "hr_report_template.html", template_vars)
    return


def get_boss_rapport(request):
    pk = request.args['pk'][0]
    user = request.user
    create_and_send_pdf(user.chat_id, "boss_report_template.html", get_data_for_rapport(pk))
    return


def get_data_for_rapport(pk):
    old_review = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Rating, Form.rating).join(Status, Form.status) \
        .filter(Form.id == pk) \
        .filter(ReviewPeriod.is_active == False).one_or_none()
    duties = Session().query(Duty).filter(Duty.form == old_review)
    projects = Session().query(Project).filter(Project.form == old_review)
    achievements = Session().query(Achievement).filter(Achievement.form == old_review)
    fails = Session().query(Fail).filter(Fail.form == old_review)
    template_vars = {"start": old_review.review_period.start_date.date(),
                     "end": old_review.review_period.end_date.date(),
                     "fullname": old_review.user.fullname,
                     "username": old_review.user.username,
                     "rating": old_review.rating.name,
                     "boss": old_review.user.boss.fullname if old_review.user.boss else 'Нет',
                     "duties": duties,
                     "projects": projects,
                     "achievements": achievements,
                     "fails": fails,
                     "summary": 'summary'}

    return template_vars


def create_and_send_pdf(chat_id, template_name, template_vars):
    filename = f"report_{datetime.datetime.now()}.pdf"
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    html_out = template.render(template_vars)
    HTML(string=html_out).write_pdf(filename)
    with open(filename, "rb") as f:
        bot.send_document(chat_id, f)

    os.remove(filename)
