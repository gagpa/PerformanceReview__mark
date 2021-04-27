from app.db import Session
from app.models import Form, ReviewPeriod, User, Status
from app.tbot.services.forms.archive_form import ArchiveForm


def old_review_list(request):
    old_reviews = Session().query(ReviewPeriod) \
        .filter(ReviewPeriod.is_active == False) \
        .order_by(ReviewPeriod.end_date.desc()).all()
    return ArchiveForm(old_reviews=old_reviews, page=request.page, review_list=True)


def old_forms_list(request):
    pk = request.args['pk'][0]
    old_forms = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(ReviewPeriod.id == pk).all()
    return ArchiveForm(old_forms=old_forms, period_id=pk, page=request.page, archive_list=True)
