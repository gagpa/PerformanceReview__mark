import telebot

from src import config
from src.models import User, db_session
from src.resources.auth import process_name_step
from src.resources.keyboards import create_reply_start_keyboard, \
    create_inline_keyboard_for_user_request, create_users_with_paginator

bot = telebot.TeleBot(config.TOKEN)


def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            message = args[0]
            user = User.lookup(message.chat.id)
            if user and (user.roles == role):
                func(*args, **kwargs)
            else:
                bot.send_message(message.chat.id, 'Доступ запрещен')

        return wrapper

    return decorator


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    if not User.lookup(message.chat.id):
        bot.send_message(chat_id,
                         'Приветствую @{}.'.format(message.chat.username))
        user = User(id=chat_id, username=f'@{message.chat.username}')
        db_session.add(user)
        bot.send_message(chat_id, 'Введите свое ФИО')
        bot.register_next_step_handler(message, process_name_step, bot)
    else:
        bot.send_message(chat_id, 'Что бы вы хотели сделать?',
                         reply_markup=create_reply_start_keyboard())


@bot.callback_query_handler(lambda call: 'requests|back' in call.data)
@bot.message_handler(func=lambda message: message.text == 'Запросы')
def all_requests(message):
    users = db_session.query(User).filter_by(roles=None).all()

    try:
        chat_id = message.chat.id
    except AttributeError:
        chat_id = message.message.chat.id
        bot.delete_message(chat_id=chat_id, message_id=message.message.message_id)

    if users:
        msg, paginator = create_users_with_paginator(users, page=1, n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'requests#' in call.data)
def all_requests(call):
    users = db_session.query(User).filter_by(roles=None).all()
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    if users:
        page = call.data.split('#')[-1]
        msg, paginator = create_users_with_paginator(users, page=int(page), n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'requests#' in call.data)
def all_requests(call):
    users = db_session.query(User).filter_by(roles=None).all()
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    if users:
        page = call.data.split('#')[-1]
        msg, paginator = create_users_with_paginator(users, page=int(page), n=2)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'requests|get' in call.data)
def show_user_request(call):
    chat_id = call.message.chat.id
    user_id = call.data.split('|')[-1]
    user = db_session.query(User).get(user_id)
    user_info = f'''
        Логин: {user.username}
        ФИО: {user.full_name}
        Должность: {user.position}
        Отдел: {user.department}
        Руководитель: {user.chef}
    '''.replace('  ', '')

    markup_inline = create_inline_keyboard_for_user_request(user_id)
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, user_info, reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: 'requests|del' in call.data)
def delete_user(call):
    chat_id = call.message.chat.id
    user_id = call.data.split('|')[-1]
    user = db_session.query(User).get(user_id)
    db_session.delete(user)
    db_session.commit()
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, f'Пользователь {user.username} отклонен')
    bot.send_message(user_id, 'Доступ отклонен')


@bot.callback_query_handler(lambda call: 'requests|add' in call.data)
def accept_user(call):
    chat_id = call.message.chat.id
    user_id = call.data.split('|')[-1]
    User.update(user_id, roles='Employee')
    db_session.commit()
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, f'Пользователь {User.identify(user_id).username} принят')
    bot.send_message(chat_id, 'Вам одобрили доступ!')
    # bot.send_document(chat_id, "file")


@bot.message_handler(commands=['ls'])
@role_required('HR')
def all_employees(message):
    chat_id = message.chat.id
    users = db_session.query(User).filter(User.roles == 'Employee').all()
    if users:
        res = {i.id: ' '.join([i.username, i.full_name, str(i.roles)]) for i in users}
        bot.send_message(chat_id, str(res))
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.message_handler(commands=['qq'])
@role_required('HR')
def check_users(message):
    chat_id = message.chat.id
    user = db_session.query(User).get(chat_id)
    db_session.delete(user)
    db_session.commit()
    bot.send_message(chat_id, 'Вы удалены из бота')


# @bot.message_handler(commands=['create'])
# def start_message(message):
#     """Create test users"""
#     for i in range(11):
#         if not User.lookup(i):
#             user = User(id=i, username=f'@username{i}', full_name=f'name{i}')
#             db_session.add(user)
#     db_session.commit()


bot.polling()
