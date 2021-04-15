from urllib.parse import parse_qs

from loguru import logger

from app.db import Session
from app.services.dictinary import StatusService
from app.services.form_review import FormService
from app.services.review import ReviewPeriodService
from app.services.user import UserService
from app.tbot.storages import ROUTES, COMMANDS


def add_user(message):
    """ Добавить пользователя в сообщение """
    chat_id = str(message.chat.id)
    user_service = UserService()
    answer = user_service.is_exist(chat_id=chat_id)
    if answer:
        user = user_service.by_chat_id(chat_id=chat_id)
    else:
        user_info = message.from_user
        user = user_service.create_default(chat_id=chat_id,
                                           username=f'{user_info.last_name}{user_info.id}',
                                           fullname=f'{user_info.last_name} {user_info.first_name}',
                                           )
    Session().commit()
    message.user = \
        {
            'is_new': not answer,
            'pk': user.id,
            'role': user.role.name,
            'have_boss': True if user.boss else False,
            'boss': user.boss.username if user.boss else None,
        }


def add_review_period(message):
    """ Добавить review преиод """
    service = ReviewPeriodService()
    answer = service.is_now
    Session().commit()
    message.review_period = \
        {
            'is_active': answer,
            'pk': service.current.id if answer else None
        }


def add_form(message):
    """ Добавить форму """
    form_service = FormService()
    if message.review_period['is_active']:
        review_period_pk = message.review_period['pk']
        if form_service.is_exist(user_id=message.user['pk'], review_period_id=review_period_pk):
            form = form_service.by(user_id=message.user['pk'], review_period_id=review_period_pk)
        else:
            status_service = StatusService()
            status = status_service.write_in
            form = form_service.create(user_id=message.user['pk'], review_period_id=review_period_pk, status=status)
        Session().commit()

        message.form = \
            {
                'is_exist': True,
                'is_full': False,
                'pk': form.id,
                'status': form.status.name,
            }
    else:
        message.form = \
            {
                'is_exist': False
            }


def add_keyboard(message):
    """ Выдача клавиатуры роле пользвателя """
    pass


def log_command(message):
    """ Логировать действия пользователей """
    user = message.user
    logger.debug(f'\nUSER {user} COMMAND: {message.command}')


def log_callback(call):
    user = call.message.user
    logger.debug(f'\nUSER {user} URL: {call.url}')


def log_unknown(message):
    """ Логировать неизвестного пользователя """
    logger.debug(f'ЗАПРОС ОТ CHAT_ID: {message.chat.id}\nMESSAGE:\n{message.text}')


def log_bot(message):
    """ Логировать действия бота """
    user = message.user
    logger.debug(f'\nUSER {user} CHAT_ID: {message.chat.id}\nBOT_CALLBACK_MESSAGE:\n{message.text}')


def parse_command(bot_instance, message):
    """ Запарсить команду и поместить её объект сообщения"""
    message.command = message.text.replace('/', '')
    message.is_exist = message.command in COMMANDS.keys()


def parse_url(bot_instance, call):
    """ Запарсить URL callback с аргумантами и поместить их в обзъект сообщения"""
    args = parse_qs(call.data)
    call.message.args = args
    call.url = args['callback'][0]
    call.is_exist = call.url in ROUTES.keys()


__all__ = \
    [
        'add_user',
        'add_review_period',
        'add_form',
        'add_keyboard',
        'log_callback',
        'log_command',
        'log_unknown',
        'log_bot',
        'parse_url',
        'parse_command'
    ]
