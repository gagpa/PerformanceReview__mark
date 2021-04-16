from app.db import Session
from app.models import Form, ReviewPeriod, User, Status, CoworkerAdvice
from app.services.dictinary.summary import SummaryService
from app.tbot.services.forms.current_review_form import CurrentReviewForm


def current_forms_list(request):
    """Получаем список форм в текущем ревью"""
    current_reviews = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(ReviewPeriod.is_active == True).all()
    if current_reviews:
        return CurrentReviewForm(models=current_reviews, forms_list=True)
    else:
        return CurrentReviewForm()


def employee_review(request):
    pk = request.pk()
    current_review = Session().query(Form).join(User, Form.user).join(Status, Form.status) \
        .filter(Form.id == pk).one_or_none()
    coworker_advices = Session().query(CoworkerAdvice).filter_by(form_id=pk).all()
    summary = SummaryService().by_form_id(pk)
    if not summary:
        return CurrentReviewForm(model=current_review, advices=coworker_advices, summary=summary)
    else:
        return CurrentReviewForm(model=current_review, advices=coworker_advices, summary=summary)


def input_summary(request):
    pk = request.args['pk'][0]
    return CurrentReviewForm(change_summary=True), request.send_args(change_summary, pk=pk)


def change_summary(request):
    pk = request.args['pk'][0]
    summary = SummaryService().by_form_id(pk)
    if not summary:
        summary = SummaryService().create(form_id=pk, from_hr_id=request.user.id, text=request.text)
    else:
        summary.text = request.text
    Session().add(summary)
    Session().commit()
    return CurrentReviewForm(changed=True)
