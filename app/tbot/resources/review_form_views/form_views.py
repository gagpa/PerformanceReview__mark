from app.tbot.extensions import MessageManager
from app.tbot.services.forms import ReviewForm
from app.services.status import change_boss_review, get_boss_review


def controller_form(message):
    """ Покзать анкету """
    form = message.form
    on_write = form.status != get_boss_review()
    template = ReviewForm(form, on_write=on_write)
    MessageManager.send_message(message=message, template=template)


def controller_send_to_boss(message):
    """ Отправить руководителю """
    form = message.form
    change_boss_review(form)
    on_write = form.status != get_boss_review()
    template = ReviewForm(form, on_write=on_write)
    MessageManager.send_message(message=message, template=template)


__all__ = \
    [
        'controller_form',
        'controller_send_to_boss',
    ]
