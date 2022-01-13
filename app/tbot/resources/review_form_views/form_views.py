from app import models
from app.db import Session
from app.models import Fail, Duty, Achievement
from app.pkgs.review_archive import ReviewArchive
from app.services.dictinary import StatusService
from app.services.form_review import FormService, ProjectsService
from app.services.user import EmployeeService
from app.tbot import notificator
from app.tbot.services.forms import ReviewForm, Notification


def form_view(request):
    """ Покзать анкету """
    if request.review_period['is_active']:
        form = request.form
        form_service = FormService(form)
        status_service = StatusService()
        write_in = form_service.is_current_status(status_service.write_in)
        template = ReviewForm(form=form, review_type='write', have_markup=write_in)
    else:
        template = ReviewForm(review_type='not_active')
    return template


def send_to_boss_view(request):
    """ Отправить руководителю """
    form = request.form
    employee = request.user
    employee_service = EmployeeService(employee)
    status_service = StatusService()
    employee_service.send_boss(form)
    if form.user.boss:
        notificator.notificate(Notification(view='to_boss', form=form), form.user.boss.chat_id)
    form_service = FormService(form)
    write_in = form_service.is_current_status(
        status_service.write_in)  # TODO не обновляется form в сессии
    template = ReviewForm(form=form, review_type='write', write_in=write_in)
    return template


def copy_last_review(request):
    """ Скопировать анкету из предыдущего ревью """
    last_form_id = request.args.get('last_form')[0]
    form_archive = ReviewArchive().find_form(last_form_id)
    user = Session.query(models.User).filter_by(username=form_archive.author.username).one()
    for form in Session().query(models.Form).filter_by(user=user).all():
        Session().delete(form)
    Session().commit()
    new_form = models.Form(user_id=user.id, review_period_id=request.review_period['pk'],
                           status_id=StatusService().write_in.id)
    form_service = FormService()
    form_service.save(new_form)
    Session.commit()
    new_form = Session().query(models.Form).filter_by(user=user).one()
    for project in form_archive.projects:
        new_project = models.Project(name=project.name, description=project.description, form=new_form)
        Session.add(new_project)
        Session.commit()
        project_service = ProjectsService(new_project)
        project_service.add_contacts([user.employee.username for user in project.respondents])
        Session.commit()

    for last_fail in form_archive.fails:
        fail = Fail(text=last_fail, form_id=new_form.id)
        Session().add(fail)
        Session.commit()

    for last_duty in form_archive.duties:
        duty = Duty(text=last_duty, form_id=new_form.id)
        Session().add(duty)
        Session.commit()

    for last_achievement in form_archive.achievements:
        achievement = Achievement(text=last_achievement, form_id=new_form.id)
        Session().add(achievement)
        Session.commit()
    return ReviewForm(form=new_form, review_type='write', have_markup=True)


__all__ = [
    'form_view',
    'send_to_boss_view',
]
