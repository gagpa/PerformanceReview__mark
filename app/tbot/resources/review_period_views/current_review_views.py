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
    return CurrentReviewForm(models=current_forms, page=request.page, forms_list=True)


def employee_review(request):
    """Информация о пользователе за текущие Review"""
    form_id = request.args['pk'][0]
    current_form = Session().query(Form).join(User, Form.user).join(Status, Form.status) \
        .filter(Form.id == form_id).one_or_none()
    advices = Session().query(CoworkerAdvice).join(CoworkerReview, Form).filter(Form.id == form_id).all()
    summary = SummaryService().by_form_id(form_id)
    rating = ProjectCommentService().final_rating(form_id)
    return CurrentReviewForm(model=current_form, advices=advices, summary=summary,
                             rating=rating, form_id=form_id)


def input_summary(request):
    """Предлагаем HR ввести summary"""
    form_id = request.args['form_id'][0]
    current_review = Session().query(Form).join(User, Form.user).join(Status, Form.status) \
        .filter(Form.id == form_id).one_or_none()
    coworker_advices = Session().query(CoworkerAdvice).join(CoworkerReview, Form).filter(Form.id == form_id).all()
    summary = SummaryService().by_form_id(form_id)
    rating = ProjectCommentService().final_rating(form_id)
    return CurrentReviewForm(model=current_review, advices=coworker_advices, summary=summary,
                             rating=rating, change_summary=True), request.send_args(change_summary,
                                                                                    form_id=form_id)


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
