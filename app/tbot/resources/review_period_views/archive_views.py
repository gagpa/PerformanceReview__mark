import datetime
import os
from statistics import mean

from jinja2 import FileSystemLoader, Environment
from weasyprint import HTML

from app.db import Session
from app.models import Form, ReviewPeriod, User, Rating, Status, Duty, Project, Achievement, Fail, \
    CoworkerAdvice
from app.services.dictinary.summary import SummaryService
from app.services.form_review.project_comments import ProjectCommentService
from app.tbot import bot
from app.tbot.services.forms.archive_form import ArchiveForm


def old_forms_list(request):
    old_reviews = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(ReviewPeriod.is_active == False).all()
    return ArchiveForm(models=old_reviews, archive_list=True)


def get_rapport(request):
    pk = request.pk()
    return ArchiveForm(pk=pk, choose_rapport=True)


def get_hr_rapport(request):
    pk = request.args['pk'][0]
    user = request.user
    template_vars = get_data_for_rapport(pk)
    final_rating = ProjectCommentService().final_rating(pk)
    template_vars.update(rating=final_rating)
    # boss_comments = ProjectCommentService().boss_projects_comments(pk)
    # boss_advices = Session().query(CoworkerAdvice)\
    #     .filter_by(form_id=pk, user_id=boss_comments.user_id).all()
    # reviews = []
    template_vars.update(reviews=[])
    create_and_send_pdf(user.chat_id, "templates/hr_report_template.html", template_vars)
    return


def get_boss_rapport(request):
    pk = request.args['pk'][0]
    user = request.user
    template_vars = get_data_for_rapport(pk)
    coworkers_comments = ProjectCommentService().coworkers_projects_comments(pk)
    coworkers_rating = [comment.rating.value for comment in coworkers_comments]
    boss_comments = ProjectCommentService().boss_projects_comments(pk)
    boss_rating = [comment.rating.value for comment in boss_comments]
    subordinate_comments = ProjectCommentService().subordinate_projects_comments(pk)
    subordinate_rating = [comment.rating.value for comment in subordinate_comments]
    final_rating = ProjectCommentService().final_rating(pk)
    template_vars.update(rating=final_rating,
                         boss_rating=mean(boss_rating) if boss_rating else None,
                         coworkers_rating=mean(coworkers_rating) if coworkers_rating else None,
                         subordinate_rating=mean(subordinate_rating) if subordinate_rating else None)
    create_and_send_pdf(user.chat_id, "templates/boss_report_template.html", template_vars)
    return


def get_data_for_rapport(pk):
    review = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(Form.id == pk).one_or_none()
    duties = Session().query(Duty).filter(Duty.form == review)
    projects = Session().query(Project).filter(Project.form == review)
    achievements = Session().query(Achievement).filter(Achievement.form == review)
    fails = Session().query(Fail).filter(Fail.form == review)
    summary = SummaryService().by_form_id(pk)
    template_vars = {"start": review.review_period.start_date.date(),
                     "end": review.review_period.end_date.date(),
                     "fullname": review.user.fullname,
                     "username": review.user.username,
                     "boss": review.user.boss.fullname if review.user.boss else 'Нет',
                     "duties": duties,
                     "projects": projects,
                     "achievements": achievements,
                     "fails": fails,
                     "summary": summary.text if summary else 'Отсутсвует'}

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
