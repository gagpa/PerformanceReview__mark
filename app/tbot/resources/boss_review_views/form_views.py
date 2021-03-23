from app.services.form import get_by_id
from app.services.status import change_emp_review
from app.tbot.extensions import MessageManager
from app.tbot.resources.boss_review_views.list_forms_views import controller_boss_review_list
from app.tbot.services.boss_review import add_wrapper
from app.tbot.services.forms import ReviewForm


def controller_boss_review_form(message):
    """ Анкета на проврке босса """
    pk = message.pk

    form = get_by_id(pk)
    template = ReviewForm(form, on_boss_review=True)

    MessageManager.send_message(message=message, template=template)


def controller_boss_review_accept(message):
    """ Принять """
    pk = message.pk
    form = get_by_id(pk)
    change_emp_review(form)
    controller_boss_review_list(message=message)


def controller_boss_review_decline(message):
    """ Отклонить """
    pk = message.pk

    form = get_by_id(pk)
    template = ReviewForm(form)
    message.model = form
    MessageManager.ask_user(message=message, template=template,
                            next_controller=add_wrapper(controller_boss_review_list))


__all__ = \
    [
        'controller_boss_review_form',
        'controller_boss_review_accept',
        'controller_boss_review_decline',
    ]
