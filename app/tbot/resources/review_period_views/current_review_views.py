from app.db import Session
from app.models import Form, ReviewPeriod, User, Status
from app.tbot.services.forms.current_review_form import CurrentReviewForm


def current_forms_list(request):
    current_reviews = Session().query(Form).join(ReviewPeriod, Form.review_period) \
        .join(User, Form.user).join(Status, Form.status) \
        .filter(ReviewPeriod.is_active == True).all()
    if current_reviews:
        return CurrentReviewForm(models=current_reviews, forms_list=True)
    else:
        return CurrentReviewForm()