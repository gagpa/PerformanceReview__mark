from app.services.achievement import get_for_pk, delete
from app.services.fail import get_for_pk, delete
from app.tbot.extensions import MessageManager
from app.tbot.resources.review_form_views.fails_views import controller_fails
from app.tbot.services.achievement import edit_wrapper
from app.tbot.services.fail import edit_wrapper
from app.tbot.services.forms import FailForm


def controller_fail_delete(message):
    """ Удлаить провал """
    pk = message.pk

    fail = get_for_pk(pk)
    delete(fail)

    controller_fails(message=message)


def controller_fail_edit(message):
    """ Изменить провал """
    pk = message.pk

    fail = get_for_pk(pk)
    template = FailForm(fail)
    message.model = fail

    MessageManager.ask_user(message=message,
                            next_controller=edit_wrapper(controller_fails),
                            template=template,
                            )


__all__ = \
    [
        'controller_fail_delete',
        'controller_fail_edit',
    ]
