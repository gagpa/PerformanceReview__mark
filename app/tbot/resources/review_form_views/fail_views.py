from app.models import Form
from app.services.fail_service import get_for_pk, delete
from app.tbot.resources.review_form_views.fails_views import controller_fails
from app.tbot.services import ask_user
from app.tbot.services.fail_service import edit_wrapper
from app.tbot.services.template_forms import FailFormTemplate


def controller_fail_delete(call, form: Form):
    """

    :param message:
    :param form:
    :return:
    """
    pk = int(call.data.split(' ')[-1])

    fail = get_for_pk(pk)
    delete(fail)

    controller_fails(message=call.message, form=form)


def controller_fail_edit(call, form: Form):
    """

    :param call:
    :param form:
    :return:
    """
    pk = int(call.data.split(' ')[-1])

    fail = get_for_pk(pk)
    template = FailFormTemplate()

    ask_user(message=call.message,
             next_controller=edit_wrapper(controller_fails),
             template=template,
             form=form,
             data=fail
             )
