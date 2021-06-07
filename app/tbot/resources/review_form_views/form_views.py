from app.db import Session
from app.models import Fail, Duty, Achievement
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
    form = request.form
    last_form_id = request.args.get('last_form')[0]

    form_service = FormService(form)
    status_service = StatusService()

    last_projects = ProjectsService().all_by(form_id=last_form_id)
    for last_project in last_projects:
        last_project_service = ProjectsService(last_project)
        new_project = ProjectsService.create_empty(form=form)
        service = ProjectsService(new_project)
        service.name = last_project_service.name
        service.description = last_project_service.description
        service.contacts = [user.username for user in last_project_service.contacts]
        Session.commit()

    last_fails = Session().query(Fail).filter_by(form_id=last_form_id).all()
    for last_fail in last_fails:
        fail = Fail(text=last_fail.text, form_id=form.id)
        Session().add(fail)
        Session.commit()

    last_duties = Session().query(Duty).filter_by(form_id=last_form_id).all()
    for last_duty in last_duties:
        duty = Duty(text=last_duty.text, form_id=form.id)
        Session().add(duty)
        Session.commit()

    last_achievements = Session().query(Achievement).filter_by(form_id=last_form_id).all()
    for last_achievement in last_achievements:
        achievement = Achievement(text=last_achievement.text, form_id=form.id)
        Session().add(achievement)
        Session.commit()

    write_in = form_service.is_current_status(status_service.write_in)

    return ReviewForm(form=form, review_type='write', have_markup=write_in)


__all__ = [
    'form_view',
    'send_to_boss_view',
]
