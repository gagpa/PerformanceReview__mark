import datetime

import telebot_calendar

from app.db import db_session
from app.models import User, Role, ReviewPeriod, Position, Department, Form
from app.tbot.create_bot import bot
from app.tbot.resources.auth import process_name_step
from app.tbot.resources.decorators import check_message
from app.tbot.resources.keyboards import create_inline_keyboard_for_user_request, \
    create_users_with_paginator, create_inline_keyboard_for_user_list, create_inline_keyboard, \
    create_reviews_with_paginator, choose_date, create_reply_start_keyboard


@bot.middleware_handler(update_types=['message', 'callback_query'])
def modify_message(bot_instance, message):
    try:
        chat_id = message.chat.id
    except:
        chat_id = message.message.chat.id
    message.user = db_session.query(User).filter_by(id=chat_id).one_or_none()
    actual_review = db_session.query(ReviewPeriod).filter_by(is_active=True).one_or_none()
    if actual_review:
        message.form = db_session.query(Form).filter_by(
            user_id=chat_id,
            review_period_id=actual_review.id
        ).one_or_none()
    else:
        message.form = None


@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.user
    if not user:
        bot.send_message(message.chat.id, 'Приветствую @{}.'.format(message.chat.username))
        user = User(id=message.chat.id, username=message.chat.username)
        bot.send_message(message.chat.id, 'Введите свое ФИО')
        bot.register_next_step_handler(message, process_name_step, user)
    else:
        bot.send_message(user.id, 'Что бы вы хотели сделать?',
                         reply_markup=create_reply_start_keyboard())


@bot.callback_query_handler(lambda call: 'requests|back' in call.data)
@bot.message_handler(func=lambda message: message.text == 'Запросы')
def all_requests(message):
    users = db_session.query(User).filter_by(role_id=0).all()

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
    users = db_session.query(User).filter_by(role_id=0).all()
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
        ФИО: {user.fullname}
        Должность: {user.position.name}
        Отдел: {user.department.name}
        Руководитель: {user.boss.username if user.boss else "Нет"}'''

    if kind == 'requests':
        markup_inline = create_inline_keyboard_for_user_request(user_id)
    else:
        user_info += f'\nРоль: {user.role.name}'
        markup_inline = create_inline_keyboard_for_user_list(user_id)

    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, user_info.replace('  ', ''), reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: 'employee|del' in call.data)
@bot.callback_query_handler(lambda call: 'requests|del' in call.data)
def delete_user(call):
    chat_id = call.message.chat.id
    user_id = call.data.split('|')[-1]
    user = db_session.query(User).filter_by(id=user_id).first()
    print(user)
    db_session.delete(user)
    db_session.commit()
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, f'Пользователь {user.username} отклонен')
    bot.send_message(user_id, 'Доступ отклонен')


@bot.callback_query_handler(lambda call: 'requests|add' in call.data)
def accept_user(call):
    chat_id = call.message.chat.id
    user_id = call.data.split('|')[-1]

    db_session.query(User).filter_by(id=user_id).update({'role_id': 1})
    db_session.commit()
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, f'Пользователь принят')
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

    users = db_session.query(User).filter(User.role_id != 0).all()
    if users:
        msg, paginator = create_users_with_paginator('employee', users, page=1, n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'employee#' in call.data)
def employees_per_page(call):
    users = db_session.query(User).filter(User.role_id != 0).all()
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
    service_dict = {'ФИО': 'fullname',
                    'Должность': 'position',
                    'Отдел': 'department',
                    'Логин руководителя': 'boss',
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
        service_dict = {'fullname': 'новое ФИО',
                        'position': 'новую должность',
                        'department': 'новый отдел',
                        'boss': 'новый логин руководителя'
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
    role = db_session.query(Role).filter_by(name=role).one()
    db_session.query(User).filter_by(id=user_id).update({'role_id': role.id})
    db_session.commit()
    bot.send_message(chat_id, 'Изменения внесены')


@check_message
def accept_data_to_change(message, call_data):
    attr_to_change = call_data.split('|')[-1]
    user_id = call_data.split('|')[-2]
    chat_id = message.chat.id
    user = db_session.query(User).get(user_id)
    if attr_to_change == 'fullname':
        user.fullname = message.text
    user = db_session.query(User).get(user_id)
    if attr_to_change == 'fullname':
        user.fullname = message.text
    elif attr_to_change == 'position':
        pos = db_session.query(Position).filter_by(name=message.text).one_or_none()
        user.position = pos if pos else Position(name=message.text)
    elif attr_to_change == 'department':
        dep = db_session.query(Department).filter_by(name=message.text).one_or_none()
        user.department = dep if dep else Department(name=message.text)
    elif attr_to_change == 'boss':
        boss_login = message.text.lower().replace('@', '')
        if boss_login != 'нет':
            boss = db_session.query(User).filter_by(username=boss_login).one_or_none()
            if boss:
                user.boss_id = boss.id
            else:
                bot.send_message(chat_id, 'Вашего руководителя еще нет в системе')
        else:
            user.boss = None

    db_session.add(user)
    db_session.commit()
    bot.send_message(chat_id, 'Изменения внесены')


@bot.message_handler(func=lambda message: message.text == 'Запуск/остановка Review')
def review(message):
    chat_id = message.chat.id
    service_dict = {'Запуск': 'start',
                    'Остановка': 'stop'
                    }
    markup_inline = create_inline_keyboard('review', service_dict)
    bot.send_message(chat_id, 'Выберите действие', reply_markup=markup_inline)


@bot.callback_query_handler(lambda call: 'review|start' in call.data)
def start_review(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    current = db_session.query(ReviewPeriod).filter_by(is_active=True).one_or_none()
    if not current:
        msg = "Выберите дату начала периода"
        choose_date(chat_id, 'review|first_date', msg)
    else:
        bot.send_message(chat_id, 'Review уже запущено')


@bot.callback_query_handler(lambda call: 'review|stop' in call.data)
def stop_review(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    current = db_session.query(ReviewPeriod).filter_by(is_active=True).one_or_none()
    print(current)
    if current:
        current.is_active = False
        db_session.add(current)
        db_session.commit()
        bot.send_message(chat_id, 'Текущие Review остановлено')
    else:
        bot.send_message(chat_id, 'Нет активных Review')


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
            print(date)
            choose_date(chat_id, f'review|{date.strftime("%Y-%m-%d %H-%M-%S")}|second|', msg)
            db_session.commit()
            print(date)
        elif 'second' in call_data:
            print(call_data)
            first_date = datetime.datetime.strptime(call_data.split('|')[1], '%Y-%m-%d %H-%M-%S')
            review_period = ReviewPeriod(start_date=first_date, end_date=date, is_active=True)
            db_session.add(review_period)
            db_session.commit()
            print(review_period)
            print(date)
            users = db_session.query(User).all()
            for user in users:
                if user.boss is not None:
                    msg = 'Необходимо заполнить анкету в разделе "Заполнение анкеты"'
                    bot.send_message(user.id, msg)
    elif action == "CANCEL":
        bot.send_message(chat_id=call.from_user.id, text="Попробуйте снова")


@bot.message_handler(func=lambda message: message.text == 'Текущий Review')
# @role_required('HR')
def current_review(message):
    current = db_session.query(ReviewPeriod).filter_by(is_active=True).one_or_none()
    chat_id = message.chat.id

    if current:
        msg, paginator = create_reviews_with_paginator('review', current, page=1, n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Review не запущен. '
                                  'Вы можете запустить его в разделе "Запуск/остановка Review"')


@bot.callback_query_handler(lambda call: 'review#' in call.data)
def employees_per_page(call):
    # TODO: change User to Review
    users = db_session.query(User).filter(User.role is not None).all()
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    if users:
        page = call.data.split('#')[-1]
        msg, paginator = create_reviews_with_paginator('review', users, page=int(page), n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.message_handler(commands=['qq'])
# @role_required('HR')
def check_users(message):
    chat_id = message.chat.id
    user = db_session.query(User).get(chat_id)
    db_session.delete(user)
    db_session.commit()
    bot.send_message(chat_id, 'Вы удалены из бота')


@bot.message_handler(commands=['create'])
def create_test_users(message):
    """Create test users"""
    for i in range(11):
        user = db_session.query(User).filter_by(id=i).one_or_none()
        if not user:
            user = User(id=i, username=f'username{i}', fullname=f'name{i}', role_id=i % 2)

            dep = db_session.query(Department).filter_by(name='Тест').one_or_none()
            user.department_id = dep.id if dep else Department(name='Тест').id
            pos = db_session.query(Position).filter_by(name='Тест').one_or_none()
            user.position_id = pos.id if pos else Position(name='Тест').id
            db_session.add(user)
            db_session.commit()


def init_roles():
    roles = ['Undefined', 'Employee', 'HR', 'Lead']
    for i, role in enumerate(roles):
        role = Role(id=i, name=role)
        db_session.add(role)
    db_session.commit()


if __name__ == '__main__':
    # init_roles()
    bot.polling()
