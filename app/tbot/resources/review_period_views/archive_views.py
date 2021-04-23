from app.db import Session
from app.models import Form, ReviewPeriod, User, Status
from app.tbot.services.forms.archive_form import ArchiveForm


def old_forms_list(request):
    old_reviews = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(ReviewPeriod.is_active == False)\
        .order_by(ReviewPeriod.end_date.desc()).all()
    return ArchiveForm(models=old_reviews, archive_list=True)
