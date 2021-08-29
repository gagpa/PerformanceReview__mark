from statistics import mean

from app.db import Session
from app.models import Form, ReviewPeriod, User, Status, CoworkerAdvice, CoworkerReview
from app.services.dictinary import StatusService
from app.services.dictinary.summary import SummaryService
from app.services.form_review import FormService
from app.services.form_review.project_comments import ProjectCommentService
from app.tbot.services.forms.current_review_form import CurrentReviewForm


def current_forms_list(request):
    """Получаем список форм в текущем ревью"""
    current_forms = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(ReviewPeriod.is_active == True).all()
    page = int(request.args['pg'][0]) if request.args.get('pg') else 1
    return CurrentReviewForm(models=current_forms, page=page, forms_list=True)


def employee_review(request):
    """Информация о пользователе за текущие Review"""
    form_id = request.args['pk'][0]
    current_form = Session().query(Form).join(User, Form.user).join(Status, Form.status) \
        .filter(Form.id == form_id).one_or_none()
    advices = Session().query(CoworkerAdvice).join(CoworkerReview, Form).filter(
        Form.id == form_id).all()
    summary = SummaryService().by_form_id(form_id)
    rating = ProjectCommentService().final_rating(form_id)

    coworkers_comments = ProjectCommentService().coworkers_projects_comments(form_id)
    coworkers_rating = [comment.rating.value for comment in coworkers_comments]
    boss_comments = ProjectCommentService().boss_projects_comments(form_id)
    boss_rating = [comment.rating.value for comment in boss_comments]
    subordinate_comments = ProjectCommentService().subordinate_projects_comments(form_id)
    subordinate_rating = [comment.rating.value for comment in subordinate_comments]

    reviews = ProjectCommentService.project_comments(form_id)

    marks = {'Руководитель': [], 'Коллеги': [], 'Подчиненные': []}
    for review in reviews:
        fullname = review.coworker.fullname
        username = review.coworker.username
        if review.coworker.id == current_form.user.boss_id:
            role = 'Руководитель'
        elif review.coworker.boss_id == current_form.user.id:
            role = 'Подчиненные'
        else:
            role = 'Коллеги'
        ratings = [project_rating.rating.value for project_rating in review.projects_ratings if
                   project_rating.rating]
        mean_rating = round(mean(ratings), 2) if ratings else 'Нет'
        marks[role].append(f'{fullname} @{username}: {mean_rating}')

    return CurrentReviewForm(
        model=current_form, advices=advices, summary=summary,
        rating=rating, form_id=form_id, marks=marks,
        boss_rating=round(mean(boss_rating), 2) if boss_rating else 'Нет',
        coworkers_rating=round(mean(coworkers_rating), 2) if coworkers_rating else 'Нет',
        subordinate_rating=round(mean(subordinate_rating), 2) if subordinate_rating else 'Нет'
    )


def input_summary(request):
    """Предлагаем HR ввести summary"""
    form_id = request.args['form_id'][0]
    current_review = Session().query(Form).join(User, Form.user).join(Status, Form.status) \
        .filter(Form.id == form_id).one_or_none()
    coworker_advices = Session().query(CoworkerAdvice).join(CoworkerReview, Form).filter(
        Form.id == form_id).all()
    summary = SummaryService().by_form_id(form_id)
    rating = ProjectCommentService().final_rating(form_id)

    coworkers_comments = ProjectCommentService().coworkers_projects_comments(form_id)
    coworkers_rating = [comment.rating.value for comment in coworkers_comments]
    boss_comments = ProjectCommentService().boss_projects_comments(form_id)
    boss_rating = [comment.rating.value for comment in boss_comments]
    subordinate_comments = ProjectCommentService().subordinate_projects_comments(form_id)
    subordinate_rating = [comment.rating.value for comment in subordinate_comments]

    reviews = ProjectCommentService.project_comments(form_id)

    marks = {'Руководитель': [], 'Коллеги': [], 'Подчиненные': []}
    for review in reviews:
        fullname = review.coworker.fullname
        username = review.coworker.username
        if review.coworker.id == current_review.user.boss_id:
            role = 'Руководитель'
        elif review.coworker.boss_id == current_review.user.id:
            role = 'Подчиненные'
        else:
            role = 'Коллеги'
        ratings = [project_rating.rating.value for project_rating in review.projects_ratings if
                   project_rating.rating]
        mean_rating = round(mean(ratings), 2) if ratings else 'Нет'
        marks[role].append(f'{fullname} @{username}: {mean_rating}')

    return CurrentReviewForm(
        model=current_review, advices=coworker_advices, summary=summary,
        rating=rating, change_summary=True, marks=marks,
        boss_rating=round(mean(boss_rating), 2) if boss_rating else 'Нет',
        coworkers_rating=round(mean(coworkers_rating), 2) if coworkers_rating else 'Нет',
        subordinate_rating=round(mean(subordinate_rating), 2) if subordinate_rating else 'Нет'
    ), request.send_args(change_summary, form_id=form_id)


def change_summary(request):
    """Записсываем summary и меняем статус формы и оценок"""
    form_id = request.args['form_id']
    summary = SummaryService().by_form_id(form_id)
    if not summary:
        SummaryService().create(form_id=form_id, from_hr_id=request.user.id,
                                text=request.text)
        form = FormService().by_pk(form_id)
        StatusService().change_to_done(form)
    else:
        summary.text = request.text
        Session.add(summary)
    Session.commit()
    request.add('pk', [form_id])
    return employee_review(request)
