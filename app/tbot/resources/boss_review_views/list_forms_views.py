from app.services.form import get_on_boss_review
from app.services.lead import get_all_employees
from app.tbot.extensions import MessageManager
from app.tbot.services.forms import ListFormReview


def controller_boss_review_list(message):
    """ Контроллер списка review начальника """
    lead = message.user
    review_period = message.review_period

    employees = get_all_employees(lead)
    forms = []
    for employee in employees:
        form = get_on_boss_review(user=employee, review_period=review_period['object'])
        if form:
            forms.append(form)
    template = ListFormReview(forms, on_boss_review=True)
    MessageManager.send_message(message=message, template=template)


__all__ = ['controller_boss_review_list']
