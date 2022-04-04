from app.services.user import HRService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ """
    hr = request.user
    service = HRService(hr)

    reviews = HRService(hr).reviews()
    forms = [review.form for review in reviews]
    template = ListFormReview(forms=forms, reviews=reviews, review='hr', page=request.page, is_asc=request.is_asc)
    return template
