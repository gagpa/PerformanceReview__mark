from app.services.user import HRService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ """
    hr = request.user
    advices = HRService(hr).advices_on_review
    template = ListFormReview(advices=advices, on_hr_review=True)
    return template
