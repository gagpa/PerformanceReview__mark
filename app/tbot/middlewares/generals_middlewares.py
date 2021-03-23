from loguru import logger

from app.services.form import is_exist as form_exist, create as create_form, get as get_form
from app.services.review_period import get_current as get_current_period, is_now as review_period_is_now
from app.services.status import get_new_form as get_status_new_form
from app.services.user import get as get_user, is_exist as user_is_exist, create_default


def add_user(message):
    """ Добавить пользователя в сообщение """
    chat_id = str(message.chat.id)
    answer = user_is_exist(chat_id=chat_id)
    if answer:
        user = get_user(chat_id=chat_id)
    else:
        user_info = message.from_user
        user = create_default(chat_id=chat_id,
                              username=f'{user_info.last_name}{user_info.id}',
                              fullname=f'{user_info.last_name} {user_info.first_name}',
                              )
    message.user = user


def add_review_period(message):
    """ Добавить review преиод """
    answer = review_period_is_now()
    message.review_period = {
        'is_active': answer,
        'object': get_current_period() if answer else None
    }


def add_form(message):
    """ Добавить форму """
    if message.review_period['is_active']:
        review_period = message.review_period['object']
        if form_exist(user=message.user, review_period=review_period):
            message.form = get_form(user=message.user, review_period=review_period)
        else:
            status = get_status_new_form()
            message.form = create_form(user=message.user, review_period=review_period, status=status)


def add_keyboard(message):
    """ Выдача клавиатуры роле пользвателя """
    # user = message.user
    # role_lead = get_lead()
    # role_employee = get_employee()
    # role_hr = get_hr()
    # btns = LEAD_BTNS
    # if user.role is role_lead:
    #     btns = LEAD_BTNS
    # elif user.role is role_employee:
    #     btns = EMPTY_KEYBOARD_BTNS
    # elif user.role is role_hr:
    #     btns = EMPTY_KEYBOARD_BTNS
    # keyboard = build_main_keyboard(btns)
    # bot.send_message(chat_id=message.chat.id, text=' TEST ', reply_markup=keyboard)
    pass


def log_user(message):
    """ Логировать действия пользователей """
    user = message.user
    logger.debug(f'\nUSER {user} CHAT_ID: {message.chat.id}\nMESSAGE:\n{message.text}')


def log_unknown(message):
    """ Логировать неизвестного пользователя """
    logger.debug(f'ЗАПРОС ОТ CHAT_ID: {message.chat.id}\nMESSAGE:\n{message.text}')


def log_bot(message):
    """ Логировать действия бота """
    user = message.user
    logger.debug(f'\nUSER {user} CHAT_ID: {message.chat.id}\nBOT_CALLBACK_MESSAGE:\n{message.text}')


def parse_pk(call):
    """ """
    parse_data = call.data.split(' ')
    pk = parse_data[-1]
    call.message.pk = int(pk) if pk.isdigit() else None
    call.data = parse_data[0]


__all__ = \
    [
        'add_user',
        'add_review_period',
        'add_form',
        'add_keyboard',
        'log_user',
        'log_unknown',
        'log_bot',
        'parse_pk'
    ]
