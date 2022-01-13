import os
from uuid import UUID

from app.pkgs.report import report_creators, create_form_frame
from app.pkgs.review_archive import ReviewArchive
from app.services.form_review import FormService
from app.services.user.user import UserService
from app.tbot import bot
from app.tbot.services.forms.archive_form import ArchiveForm


def get_rapport(request):
    pk = request.args['pk'][0]
    if pk.isdigit():
        form = create_form_frame(FormService().by_pk(pk))
    else:
        form = ReviewArchive().find_form(UUID(pk))
    return ArchiveForm(pk=form.id, period_id=form.review, choose_rapport=True)


def get_boss_rapport(request):
    pk = request.args['form_id'][0]
    if pk.isdigit():
        form_frame = create_form_frame(FormService().by_pk(pk))
    else:
        form_frame = ReviewArchive().find_form(UUID(pk))
    filename = report_creators.ReportCreatorForLead(form_frame).create()
    user = request.user
    with open(filename, 'rb') as f:
        bot.send_document(user.chat_id, f)


def send_rapport_to_boss(request):
    pk = request.args['form_id'][0]

    if pk.isdigit():
        form_frame = create_form_frame(FormService().by_pk(pk))
    else:
        form_frame = ReviewArchive().find_form(UUID(pk))
    if not form_frame.author.lead:
        return ArchiveForm(no_boss=True)
    user = UserService().by(username=form_frame.author.lead.username)
    filename = report_creators.ReportCreatorForLead(form_frame).create()
    with open(filename, 'rb') as f:
        bot.send_document(user.chat_id, f)
    os.remove(filename)
    return ArchiveForm(sent_to_boss=True)


def get_hr_rapport(request):
    pk = request.args['form_id'][0]
    if pk.isdigit():
        form_frame = create_form_frame(FormService().by_pk(pk))
    else:
        form_frame = ReviewArchive().find_form(UUID(pk))
    filename = report_creators.ReportCreatorForHR(form_frame).create()
    user = request.user
    with open(filename, 'rb') as f:
        bot.send_document(user.chat_id, f)
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
