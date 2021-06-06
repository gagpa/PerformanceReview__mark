from app.services.user import HRService
from app.tbot.services.forms import ListFormReview


def list_forms_view(request):
    """ """
    hr = request.user
    service = HRService(hr)
    if request.args.get('asc'):
        if request.args['asc'][0] == 'True':
            is_asc = True
        else:
            is_asc = False
    else:
        is_asc = True
    reviews = HRService(hr).reviews()
    forms = [review.form for review in reviews]
    page = int(request.args['pg'][0]) if request.args.get('pg') else 1
    template = ListFormReview(forms=forms, reviews=reviews, review='hr', page=page, is_asc=is_asc)
    return template
