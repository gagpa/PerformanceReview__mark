from app.services.form import get_by_id
from app.tbot.extensions import MessageManager
from app.tbot.services.forms import ReviewForm


def controller_coworker_review_form(message):
    """ Анкета на проврке коллеги """
    pk = message.pk

    form = get_by_id(pk)
    template = ReviewForm(form, on_coworker_review=True)

    MessageManager.send_message(message=message, template=template)


__all__ = ['controller_coworker_review_form']
