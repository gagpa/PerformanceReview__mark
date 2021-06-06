import datetime
import os
from statistics import mean

from jinja2 import FileSystemLoader, Environment
from weasyprint import HTML

from app.db import Session
from app.models import Form, ReviewPeriod, User, Status, Duty, Project, Achievement, Fail
from app.services.dictinary.summary import SummaryService
from app.services.form_review import FormService
from app.services.form_review.project_comments import ProjectCommentService
from app.tbot import bot
from app.tbot.services.forms.archive_form import ArchiveForm
from configs.bot_config import HR_REPORT_TEMPLATE, BOSS_REPORT_TEMPLATE


def get_rapport(request):
    pk = request.args['pk'][0]
    period_id = request.args.get('period_id')[0] if request.args.get('period_id') else None
    return ArchiveForm(pk=pk, period_id=period_id, choose_rapport=True)


def get_boss_rapport(request):
    pk = request.args['form_id'][0]
    user = request.user
    template_vars = update_data_for_boss_rapport(pk)
    create_and_send_pdf(user.chat_id, BOSS_REPORT_TEMPLATE, template_vars)


def send_rapport_to_boss(request):
    pk = request.args['form_id'][0]
    user = request.user
    template_vars = update_data_for_boss_rapport(pk)
    create_and_send_pdf(user.chat_id, BOSS_REPORT_TEMPLATE, template_vars)


def get_hr_rapport(request):
    pk = request.args['form_id'][0]
    template_vars = get_data_for_rapport(pk)
    final_rating = ProjectCommentService().final_rating(pk)
    template_vars.update(rating=final_rating if final_rating else 'Нет')

    reviews = ProjectCommentService.project_comments(pk)
    template_vars.update(reviews=[])

    form = FormService().by_pk(pk)

    for review in reviews:
        fullname = review.coworker.fullname
        if review.coworker.id == form.user.boss_id:
            role = 'Руководитель'
        elif review.coworker.boss_id == form.user.id:
            role = 'Подчиненный'
        else:
            role = 'Коллега'
        ratings = [project_rating.rating.value for project_rating in review.projects_ratings if
                   project_rating.rating]
        mark = ' + '.join(map(str, ratings))
        if len(ratings) > 1:
            mark = f'{mark} = {round(mean(ratings), 2)}'

        comments = '<br>• '.join([project_rating.text for project_rating in review.projects_ratings if project_rating.rating])
        comments = f'Комментарии по проектам:<br>• {comments}<br>'
        todo = '<br>• '.join([advice.text for advice in review.advices if advice.advice_type.name == 'todo'])
        todo = f'Что делать:<br>• {todo}<br>'
        not_todo = '<br>• '.join([advice.text for advice in review.advices if advice.advice_type.name == 'not todo'])
        not_todo = f'Что перестать делать:<br>• {not_todo}'
        template_vars['reviews'].append([fullname, role, mark, comments, todo, not_todo])

    create_and_send_pdf(request.user.chat_id, HR_REPORT_TEMPLATE, template_vars)


def update_data_for_boss_rapport(pk):
    template_vars = get_data_for_rapport(pk)
    coworkers_comments = ProjectCommentService().coworkers_projects_comments(pk)
    coworkers_rating = [comment.rating.value for comment in coworkers_comments]
    boss_comments = ProjectCommentService().boss_projects_comments(pk)
    boss_rating = [comment.rating.value for comment in boss_comments]
    subordinate_comments = ProjectCommentService().subordinate_projects_comments(pk)
    subordinate_rating = [comment.rating.value for comment in subordinate_comments]
    final_rating = ProjectCommentService().final_rating(pk)
    template_vars.update(rating=final_rating if final_rating else 'Нет',
                         boss_rating=mean(boss_rating) if boss_rating else 'Нет',
                         coworkers_rating=mean(coworkers_rating) if coworkers_rating else 'Нет',
                         subordinate_rating=mean(
                             subordinate_rating) if subordinate_rating else 'Нет')
    return template_vars


def get_data_for_rapport(pk):
    review = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(Form.id == pk).one_or_none()
    duties = Session().query(Duty).filter(Duty.form == review)
    projects = Session().query(Project).filter(Project.form == review)
    achievements = Session().query(Achievement).filter(Achievement.form == review)
    fails = Session().query(Fail).filter(Fail.form == review)
    summary = SummaryService().by_form_id(pk)
    template_vars = {'start': review.review_period.start_date.date(),
                     'end': review.review_period.end_date.date(),
                     'fullname': review.user.fullname,
                     'username': review.user.username,
                     'boss': review.user.boss.fullname if review.user.boss else 'Нет',
                     'duties': duties,
                     'projects': projects,
                     'achievements': achievements,
                     'fails': fails,
                     'summary': summary.text if summary else 'Отсутствует'}

    return template_vars


def create_and_send_pdf(chat_id, template_name, template_vars):
    filename = f'report_{datetime.datetime.now()}.pdf'
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    html_out = template.render(template_vars)
    HTML(string=html_out).write_pdf(filename)
    with open(filename, 'rb') as f:
        bot.send_document(chat_id, f)

    os.remove(filename)
