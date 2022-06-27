import typing
from statistics import mean

from app import schemas
from app.models import Form
from .. import mark_calculator as calculators


def create_form_frame(form: Form):
    """Создать слепок анкеты"""
    return schemas.FormFrame(id=form.id,
                             review=create_review_frame(form),
                             author=create_author_frame(form),
                             projects=create_projects_frames(form),
                             fails=create_fails_frames(form),
                             achievements=create_achievements_frames(form),
                             duties=create_duties_frames(form),
                             respondents=create_respondents_frames(form),
                             summary=create_summary_frames(form),
                             )


def create_review_frame(form) -> schemas.Review:
    return schemas.Review(
        id=form.review_period_id,
        start_date=form.review_period.start_date,
        end_date=form.review_period.end_date,
    )


def create_author_frame(form) -> schemas.EmployeeWithLead:
    author = form.user
    lead = author.boss
    if lead:
        lead = schemas.EmployeeWithRelation(fullname=lead.fullname,
                                            username=lead.username,
                                            department=lead.department.name,
                                            position=lead.position.name,
                                            relation=determine_relation(author, lead)
                                            )
    return schemas.EmployeeWithLead(fullname=author.fullname,
                                    username=author.username,
                                    department=author.department.name,
                                    position=author.position.name,
                                    lead=lead,
                                    )


def determine_relation(user, other_user) -> schemas.Relation:
    if user.boss and user.boss.chat_id == other_user.chat_id:
        return schemas.Relation.lead
    elif other_user.boss and other_user.boss.chat_id == user.chat_id:
        return schemas.Relation.subordinates
    return schemas.Relation.coworker


def create_projects_frames(form: Form) -> typing.List[schemas.Project]:
    projects = form.projects
    projects_frames = []
    author = form.user
    for project in projects:
        respondents = []
        for rate in project.ratings:
            mark = rate.rating.value if rate.rating else None
            employee = rate.coworker_review.coworker
            respondents.append(
                schemas.ProjectRespondent(
                    mark=mark,
                    comment=rate.text,
                    employee=schemas.EmployeeWithRelation(
                        username=employee.username,
                        fullname=employee.fullname,
                        department=employee.department.name,
                        position=employee.position.name,
                        relation=determine_relation(author, employee)
                    )
                )
            )
        projects_frames.append(schemas.Project(name=project.name,
                                               description=project.description,
                                               respondents=respondents,
                                               )
                               )
    return projects_frames


def create_fails_frames(form: Form) -> typing.List[str]:
    return [fail.text for fail in form.fails]


def create_achievements_frames(form: Form) -> typing.List[str]:
    return [achievement.text for achievement in form.achievements]


def create_duties_frames(form: Form) -> typing.List[str]:
    return [duty.text for duty in form.duties]


def create_respondents_frames(form: Form) -> typing.List[schemas.FormRespondent]:
    respondents_frames = []
    author = form.user
    for review in form.coworker_reviews:
        employee = review.coworker
        advices = review.advices
        marks = []
        marks_value = []
        for rate in review.projects_ratings:
            marks.append(schemas.ProjectMark(name=rate.project.name,
                                             description=rate.project.description,
                                             mark=rate.rating.value if rate.rating else None,
                                             comment=rate.text
                                             )
                         )
            if rate.rating and rate.rating.value > 0:
                marks_value.append(rate.rating.value)
        average_mark = round(mean(marks_value), 2) if marks_value else None
        respondent = schemas.FormRespondent(
            employee=schemas.EmployeeWithRelation(
                username=employee.username,
                fullname=employee.fullname,
                position=employee.position.name,
                department=employee.department.name,
                relation=determine_relation(author, employee),
            ),
            todo=[advice.text for advice in advices if
                  advice.advice_type.name == 'todo'],
            not_todo=[advice.text for advice in advices if
                      advice.advice_type.name == 'not todo'],
            marks=marks,
            average_mark=average_mark
        )
        respondents_frames.append(respondent)
    return respondents_frames


def create_summary_frames(form: Form) -> typing.Optional[schemas.Summary]:
    summary = form.summary
    hr = None
    text = None
    if summary:
        hr_model = summary.hr
        hr = schemas.Employee(fullname=hr_model.fullname,
                              username=hr_model.username,
                              department=hr_model.department.name,
                              position=hr_model.position.name,
                              )
        text = summary.text
    return schemas.Summary(hr=hr,
                           text=text,
                           marks=schemas.Marks(lead=calculators.LeadCalculator.calculate(form),
                                               coworkers=calculators.CoworkerCalculator.calculate(form),
                                               subordinates=calculators.SubordinateCalculator.calculate(form),
                                               total=calculators.GeneralCalculator.calculate(form)
                                               )
                           )
