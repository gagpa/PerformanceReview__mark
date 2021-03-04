import datetime

import telebot
import telebot_calendar

from src import config
from src.models import User, db_session
from src.resources.auth import process_name_step
from src.resources.keyboards import create_reply_start_keyboard, \
    create_inline_keyboard_for_user_request, create_users_with_paginator, \
    create_inline_keyboard_for_user_list, create_inline_keyboard

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


def check_message(func):
    def wrapper(*args, **kwargs):
        message = args[0]
        if message.text.lower().strip() not in ['отмена', 'список сотрудников', 'запросы',
                                                'запуск/остановка review']:
            func(*args, **kwargs)
        else:
            bot.send_message(message.chat.id, 'Внесение изменений отменено. Попробуйте снова')

    return wrapper


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
        msg, paginator = create_users_with_paginator('requests', users, page=1, n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'requests#' in call.data)
def requests_per_page(call):
    users = db_session.query(User).filter_by(roles=None).all()
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    if users:
        page = call.data.split('#')[-1]
        msg, paginator = create_users_with_paginator('requests', users, page=int(page), n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'employee|get' in call.data)
@bot.callback_query_handler(lambda call: 'requests|get' in call.data)
def show_user_request(call):
    chat_id = call.message.chat.id
    kind, _, user_id = call.data.split('|')
    user = db_session.query(User).get(user_id)
    user_info = f'''
        Логин: {user.username}
        ФИО: {user.full_name}
        Должность: {user.position}
        Отдел: {user.department}
        Руководитель: {user.chef}'''

    if kind == 'requests':
        markup_inline = create_inline_keyboard_for_user_request(user_id)
    else:
        user_info += f'\nРоль: {user.roles}'
        markup_inline = create_inline_keyboard_for_user_list(user_id)

    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, user_info.replace('  ', ''), reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: 'employee|del' in call.data)
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


@bot.callback_query_handler(lambda call: 'employee|back' in call.data)
@bot.message_handler(func=lambda message: message.text == 'Список сотрудников')
# @role_required('HR')
def all_employees(message):
    try:
        chat_id = message.chat.id
    except AttributeError:
        chat_id = message.message.chat.id
        bot.delete_message(chat_id=chat_id, message_id=message.message.message_id)

    users = db_session.query(User).filter(User.roles is not None).all()
    if users:
        msg, paginator = create_users_with_paginator('employee', users, page=1, n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'employee#' in call.data)
def employees_per_page(call):
    users = db_session.query(User).filter(User.roles is not None).all()
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    if users:
        page = call.data.split('#')[-1]
        msg, paginator = create_users_with_paginator('employee', users, page=int(page), n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'employee|change' in call.data
                                         and len(call.data.split('|')) == 3)
# @role_required('HR')
def change_employee(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    service_dict = {'ФИО': 'full_name',
                    'Должность': 'position',
                    'Отдел': 'department',
                    'Логин руководителя': 'chef',
                    'Роль': 'roles'
                    }
    markup_inline = create_inline_keyboard(call.data, service_dict)
    bot.send_message(chat_id, 'Выберите данные для изменения', reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: 'employee|change' in call.data
                                         and len(call.data.split('|')) == 4)
# @role_required('HR')
def change_employee(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    attr = call.data.split("|")[-1]
    if attr != 'roles':
        service_dict = {'full_name': 'новое ФИО',
                        'position': 'новую должность',
                        'department': 'новый отдел',
                        'chef': 'новый логин руководителя'
                        }
        bot.send_message(chat_id, f'Введите {service_dict[attr]}')
        bot.register_next_step_handler_by_chat_id(chat_id, accept_data_to_change, call.data)
    else:
        service_dict = {'HR': 'HR',
                        'Lead': 'Lead',
                        'Employee': 'Employee'
                        }
        markup_inline = create_inline_keyboard(call.data, service_dict)
        bot.send_message(chat_id, 'Выберите роль', reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: 'employee|change' in call.data and 'roles' in call.data)
def accept_role_to_change(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    role = call.data.split('|')[-1]
    user_id = call.data.split('|')[-3]
    User.update(user_id, roles=role)
    db_session.commit()
    bot.send_message(chat_id, 'Изменения внесены')


@check_message
def accept_data_to_change(message, call_data):
    attr_to_change = call_data.split('|')[-1]
    user_id = call_data.split('|')[-2]
    chat_id = message.chat.id
    User.update(user_id, **{attr_to_change: message.text})
    db_session.commit()
    bot.send_message(chat_id, 'Изменения внесены')


@bot.message_handler(func=lambda message: message.text == 'Запуск/остановка Review')
def review(message):
    chat_id = message.chat.id
    service_dict = {'Запуск': 'start',
                    'Останвока': 'stop'
                    }
    markup_inline = create_inline_keyboard('review', service_dict)
    bot.send_message(chat_id, 'Выберите действие', reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: 'review|start' in call.data)
def start_review(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    msg = "Выберите дату начала периода"
    choose_date(chat_id, 'review|first_date', msg)


@bot.callback_query_handler(lambda call: 'review|stop' in call.data)
def stop_review(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, 'Текущие Review остановлено')


def choose_date(chat_id, call_data, msg):
    now = datetime.datetime.now()
    # документация по календарю: https://github.com/FlymeDllVa/telebot-calendar
    calendar = telebot_calendar.CallbackData(call_data, "action", "year", "month", "day")
    bot.send_message(chat_id, msg,
                     reply_markup=telebot_calendar.create_calendar(name=calendar.prefix,
                                                                   year=now.year,
                                                                   month=now.month))


@bot.callback_query_handler(lambda call: any(element in call.data for element in
                                             ["PREVIOUS-MONTH", "DAY", "NEXT-MONTH", "MONTHS",
                                              "MONTH", "CANCEL", "IGNORE"]))
def callback_inline(call):
    chat_id = call.message.chat.id
    call_data, action, year, month, day = call.data.split(':')
    # Обработка календаря. Получить дату или None, если кнопки другого типа
    date = telebot_calendar.calendar_query_handler(
        bot=bot, call=call, name=call_data, action=action, year=year, month=month, day=day
    )
    if action == "DAY":
        if 'first_date' in call_data:
            msg = "Выберите дату конца периода"
            choose_date(chat_id, 'review|second_date', msg)
            print(date)
        elif 'second_date' in call_data:
            print(date)
            users = db_session.query(User).all()
            for user in users:
                if user.chef not in ['Нет', None]:
                    msg = 'Необходимо заполнить анкету в разделе "Заполнение анкеты"'
                    bot.send_message(user.id, msg)
    elif action == "CANCEL":
        bot.send_message(chat_id=call.from_user.id, text="Попробуйте снова")


@bot.message_handler(commands=['qq'])
@role_required('HR')
def check_users(message):
    chat_id = message.chat.id
    user = db_session.query(User).get(chat_id)
    db_session.delete(user)
    db_session.commit()
    bot.send_message(chat_id, 'Вы удалены из бота')


# @bot.message_handler(commands=['create'])
# def create_test_users(message):
#     """Create test users"""
#     for i in range(11):
#         if not User.lookup(i):
#             user = User(id=i, username=f'@username{i}', full_name=f'name{i}', roles='Employee')
#             db_session.add(user)
#     db_session.commit()


bot.polling()
