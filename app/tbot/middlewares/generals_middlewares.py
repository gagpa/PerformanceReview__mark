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
        message.user = \
            {
                'is_new': not answer,
                'is_exist': True,
                'pk': user.id,
                'role': user.role.name,
                'have_boss': True if user.boss else False,
                'boss': user.boss.username if user.boss else None,
            }
    else:
        message.user = {
            'is_exist': False
        }


def check_permission(bot, message):
    if message.text:
        if message.user['is_exist']:
            if message.user['role'] == 'Undefined':
                message.command = 'start'
                bot.send_message(message.chat.id, 'Дождитесь окончания регистрации')
            elif message.user['role'] == 'Employee':
                if message.command not in ['start', 'Заполнение анкеты', 'Оценка коллег']:
                    message.command = 'wrong'
            elif message.user['role'] == 'Lead':
                if message.command not in ['start', 'Заполнение анкеты', 'Оценка подчиненных', 'Оценка коллег']:
                    message.command = 'wrong'
            elif message.user['role'] == 'HR':
                if message.command == 'Оценка подчиненных':
                    message.command = 'wrong'
        elif message.text.replace('/', '') in COMMANDS.keys():
            message.is_exist = True
            message.command = 'start'
        else:
            message.command = 'start'


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
    if message.review_period['is_active'] and message.user['is_exist']:
        review_period_pk = message.review_period['pk']
        if form_service.is_exist(user_id=message.user['pk'], review_period_id=review_period_pk):
            form = form_service.by(user_id=message.user['pk'], review_period_id=review_period_pk)
        else:
            status_service = StatusService()
            status = status_service.write_in
            form = form_service.create(user_id=message.user['pk'],
                                       review_period_id=review_period_pk, status=status)
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
    if message.user['is_exist'] and message.text:
        logger.debug(f'\nUSER {user} COMMAND: {message.command}')


def log_callback(call):
    try:
        args = call.message.args
    except AttributeError:
        args = ''
    user = call.message.user
    logger.debug(f'\nUSER {user} URL: {call.url} ARGS: {args}')


def log_unknown(message):
    """ Логировать неизвестного пользователя """
    logger.debug(f'ЗАПРОС ОТ CHAT_ID: {message.chat.id}\nMESSAGE:\n{message.text}')


def log_bot(message):
    """ Логировать действия бота """
    user = message.user
    logger.debug(
        f'\nUSER {user} CHAT_ID: {message.chat.id}\nBOT_CALLBACK_MESSAGE:\n{message.text}')


def parse_command(bot_instance, message):
    """ Запарсить команду и поместить её объект сообщения"""
    if message.text:
        if message.user['is_exist']:
            message.command = message.text.replace('/', '')
            message.is_exist = message.command in COMMANDS.keys()
        elif message.text.replace('/', '') in COMMANDS.keys():
            message.is_exist = True
            message.command = 'start'
        else:
            message.is_exist = False
    else:
        message.is_exist = False


def parse_url(bot_instance, call):
    """ Запарсить URL callback с аргумантами и поместить их в обзъект сообщения"""
    # if call.message.user['is_exist']:
    if ':' in call.data:  # TODO: решить проблему с сепаратором
        args = dict()
        args['calendar'] = call.data
        if '|' in call.data:
            args['cb'], args['first_date'] = call.data.split(':')[0].split('|')
        else:
            args['cb'] = call.data.split(':')[0]
        args['call'] = call
        call.url = args['cb']
    else:
        args = parse_qs(call.data)
        call.url = args['cb'][0]

    call.message.args = args
    call.is_exist = call.url in ROUTES.keys()
    # else:
    #     call.url = 'auth'


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
        'parse_command',
        'check_permission'
    ]
