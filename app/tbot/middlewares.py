from app.services.form_service import is_exist as form_exist, create as create_form, get as get_form
from app.services.review_service import get_current as get_current_period
from app.services.status_service import get_for_new_form as get_status_for_new_form
from app.services.user_service import get as get_user
from app.tbot import bot


@bot.middleware_handler(update_types=['callback_query'])
def modify_call(bot_instance, call):
    """

    :param bot_instance:
    :param call:
    :return:
    """
    call.user = get_user(chat_id=call.message.chat.id)
    review_period = get_current_period()
    if form_exist(user=call.user, review_period=review_period):
        call.form = get_form(user=call.user, review_period=review_period)
    else:
        status = get_status_for_new_form()
        call.form = create_form(user=call.user, review_period=review_period, status=status)


@bot.middleware_handler(update_types=['message'])
def modify_message(bot_instance, call):
    """
    :param bot_instance:
    :param call:
    :return:
    """
    call.user = get_user(chat_id=str(call.chat.id))
    review_period = get_current_period()
    if form_exist(user=call.user, review_period=review_period):
        call.form = get_form(user=call.user, review_period=review_period)
    else:
        status = get_status_for_new_form()
        call.form = create_form(user=call.user, review_period=review_period, status=status)
