from app.services.user import HRService
from app.tbot.services.forms import ListFormReview
from math import ceil


def list_forms_view(request):
    """ """
    hr = request.user
    if request.args.get('asc'):
        if request.args['asc'][0] == 'True':
            is_asc = True
        else:
            is_asc = False
    else:
        is_asc = True

    page = int(request.args['pg'][0]) if request.args.get('pg') else 1
    advices = HRService(hr).advices_on_review(is_asc=is_asc)
    max_row = 2
    max_page = ceil(len(advices) / max_row)
    advices = advices[max_row * (page-1): max_row * page]

    template = ListFormReview(advices=advices, page=page, max_page=max_page, is_asc=is_asc, on_hr_review=True)
    return template
