from app.services.review.archive import get_reviews, get_review
from app.tbot.services.forms.archive_form import ArchiveForm


def old_review_list(request):
    reviews = get_reviews()
    return ArchiveForm(old_reviews=reviews, page=request.page, review_list=True)


def old_forms_list(request):
    pk = request.args['pk'][0]
    old_forms = get_review(pk)
    return ArchiveForm(old_forms=old_forms, period_id=pk, page=request.page, archive_list=True)
