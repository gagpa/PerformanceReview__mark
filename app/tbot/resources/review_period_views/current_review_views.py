from app.db import Session
from app.models import Form, ReviewPeriod, User, Status, CoworkerAdvice, Project, \
    CoworkerProjectRating, CoworkerReview
from app.services.dictinary import StatusService, HrReviewStatusService
from app.services.dictinary.summary import SummaryService
from app.services.form_review import FormService
from app.services.form_review.project_comments import ProjectCommentService
from app.services.review import CoworkerReviewService
from app.tbot.services.forms.current_review_form import CurrentReviewForm


def current_forms_list(request):
    """Получаем список форм в текущем ревью"""
    current_reviews = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(ReviewPeriod.is_active == True).all()

    return CurrentReviewForm(models=current_reviews, forms_list=True)


def employee_review(request):
    """Информация о пользователе за текущие Review"""
    pk = request.pk()
    current_review = Session().query(Form).join(User, Form.user).join(Status, Form.status) \
        .filter(Form.id == pk).one_or_none()
    coworker_advices = Session().query(CoworkerAdvice).filter_by(form_id=pk).all()
    # TODO: добавить проверку для кнопки Summary на то, что все коллеги оценили проекты
    summary = SummaryService().by_form_id(pk)
    rating = ProjectCommentService().final_rating(pk)
    return CurrentReviewForm(model=current_review, advices=coworker_advices, summary=summary,
                             rating=rating)


def input_summary(request):
    """Предлагаем HR ввести summary"""
    pk = request.args['pk'][0]
    return CurrentReviewForm(change_summary=True), request.send_args(change_summary, pk=pk)


def change_summary(request):
    """Записсываем summary и меняем статус формы и оценок"""
    pk = request.args['pk'][0]
    summary = SummaryService().by_form_id(pk)
    if not summary:
        summary = SummaryService().create(form_id=pk, from_hr_id=request.user.id,
                                          text=request.text)
        form = FormService().by_pk(pk)
        StatusService().change_to_done(form)
        # TODO: изменять статус у оценок
        # advices = CoworkerReviewService().all_by(form_id=pk)
        # ratings = Session.query(CoworkerProjectRating). \
        #     join(Project, CoworkerProjectRating.project).\
        #     join(CoworkerReview)\
        #     .filter(Project.form_id == pk).all()
        # print(ratings)
        # for rating in ratings:
        #     rating.hr_review_status = HrReviewStatusService().accept
        #     print(rating.hr_review_status)
        #     Session.add(rating)
        #     Session.commit()

    else:
        summary.text = request.text
    Session.add(summary)
    Session.commit()
    return CurrentReviewForm(changed=True)
