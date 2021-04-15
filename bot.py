import datetime
import os

import telebot_calendar
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app.db import Session
from app.models import User, Role, ReviewPeriod, Position, Department, Form
from app.tbot import bot
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
    user = Session().query(User).filter_by(id=chat_id).one_or_none()
    message.user = user if user else None
    actual_review = Session().query(ReviewPeriod).filter_by(is_active=True).one_or_none()
    if actual_review:
        message.form = Session().query(Form).filter_by(
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
        user = User(chat_id=message.chat.id, username=message.chat.username)
        bot.send_message(message.chat.id, 'Введите свое ФИО')
        bot.register_next_step_handler(message, process_name_step, user)
    else:
        bot.send_message(user.id, 'Что бы вы хотели сделать?',
                         reply_markup=create_reply_start_keyboard())


@bot.callback_query_handler(lambda call: 'requests|back' in call.data)
@bot.message_handler(func=lambda message: message.text == 'Запросы')
def all_requests(message):
    users = Session().query(User).filter_by(role_id=0).all()

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
    users = Session().query(User).filter_by(role_id=0).all()
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
    user = Session().query(User).get(user_id)
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
    user = Session().query(User).filter_by(id=user_id).first()
    print(user)
    Session().delete(user)
    Session().commit()
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    bot.send_message(chat_id, f'Пользователь {user.username} отклонен')
    bot.send_message(user_id, 'Доступ отклонен')


@bot.callback_query_handler(lambda call: 'requests|add' in call.data)
def accept_user(call):
    chat_id = call.message.chat.id
    user_id = call.data.split('|')[-1]

    Session().query(User).filter_by(id=user_id).update({'role_id': 1})
    Session().commit()
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

    users = Session().query(User).filter(User.role_id != 0).all()
    if users:
        msg, paginator = create_users_with_paginator('employee', users, page=1, n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Пользователей не найдено')


@bot.callback_query_handler(lambda call: 'employee#' in call.data)
def employees_per_page(call):
    users = Session().query(User).filter(User.role_id != 0).all()
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
    role = Session().query(Role).filter_by(name=role).one()
    Session().query(User).filter_by(id=user_id).update({'role_id': role.id})
    Session().commit()
    bot.send_message(chat_id, 'Изменения внесены')


@check_message
def accept_data_to_change(message, call_data):
    attr_to_change = call_data.split('|')[-1]
    user_id = call_data.split('|')[-2]
    chat_id = message.chat.id
    user = Session().query(User).get(user_id)
    if attr_to_change == 'fullname':
        user.fullname = message.text
    user = Session().query(User).get(user_id)
    if attr_to_change == 'fullname':
        user.fullname = message.text
    elif attr_to_change == 'position':
        pos = Session().query(Position).filter_by(name=message.text).one_or_none()
        user.position = pos if pos else Position(name=message.text)
    elif attr_to_change == 'department':
        dep = Session().query(Department).filter_by(name=message.text).one_or_none()
        user.department = dep if dep else Department(name=message.text)
    elif attr_to_change == 'boss':
        boss_login = message.text.lower().replace('@', '')
        if boss_login != 'нет':
            boss = Session().query(User).filter_by(username=boss_login).one_or_none()
            if boss:
                user.boss_id = boss.id
            else:
                bot.send_message(chat_id, 'Вашего руководителя еще нет в системе')
        else:
            user.boss = None

    Session().add(user)
    Session().commit()
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
    current = Session().query(ReviewPeriod).filter_by(is_active=True).one_or_none()
    if not current:
        msg = "Выберите дату начала периода"
        choose_date(chat_id, 'review|first_date', msg)
    else:
        bot.send_message(chat_id, 'Review уже запущено')


@bot.callback_query_handler(lambda call: 'review|stop' in call.data)
def stop_review(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    current = Session().query(ReviewPeriod).filter_by(is_active=True).one_or_none()
    print(current)
    if current:
        current.is_active = False
        Session().add(current)
        Session().commit()
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
            choose_date(chat_id, f'review|{date.strftime("%Y-%m-%d %H-%M-%S")}|second|', msg)
        elif 'second' in call_data:
            first_date = datetime.datetime.strptime(call_data.split('|')[1], '%Y-%m-%d %H-%M-%S')
            review_period = ReviewPeriod(start_date=first_date, end_date=date, is_active=True)
            Session().add(review_period)
            Session().commit()
            users = Session().query(User).all()
            for user in users:
                if user.boss is not None:
                    msg = 'Необходимо заполнить анкету в разделе "Заполнение анкеты"'
                    bot.send_message(user.id, msg)
    elif action == "CANCEL":
        bot.send_message(chat_id=call.from_user.id, text="Попробуйте снова")


@bot.message_handler(func=lambda message: message.text == 'Текущий Review')
# @role_required('HR')
def current_review(message):
    chat_id = message.chat.id
    current = Session().query(Form).join(ReviewPeriod).filter(
        Form.review_period_id == ReviewPeriod.id).filter(ReviewPeriod.is_active == True).all()
    print(current)

    if current:
        msg, paginator = create_reviews_with_paginator('review', current, page=1, n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Review не запущен. '
                                  'Вы можете запустить его в разделе "Запуск/остановка Review"')


@bot.callback_query_handler(lambda call: 'review#' in call.data)
def current_review_per_page(call):
    current = Session().query(Form).join(ReviewPeriod).filter(
        Form.review_period_id == ReviewPeriod.id).filter(ReviewPeriod.is_active == True).all()
    chat_id = call.message.chat.id
    # bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    if current:
        page = call.data.split('#')[-1]
        msg, paginator = create_reviews_with_paginator('review', current, page=int(page), n=5)
        # bot.send_message(chat_id, msg, reply_markup=paginator.markup)
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Review не запущен. '
                                  'Вы можете запустить его в разделе "Запуск/остановка Review"')


@bot.callback_query_handler(lambda call: 'review|rapport' in call.data)
# @role_required('HR')
def get_current_rapport(call):
    # form_id = call.data.split('|')[-1]
    template_vars = {"start": "1.11",
                     "end": "11.11",
                     "reviews": [0, 1, 2]}
    create_and_send_pdf(call.message.chat.id, "hr_report_template.html", template_vars)


def create_and_send_pdf(chat_id, template_name, template_vars):
    filename = f"report_{datetime.datetime.now()}.pdf"
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    html_out = template.render(template_vars)
    HTML(string=html_out).write_pdf(filename)
    with open(filename, "rb") as f:
        bot.send_document(chat_id, f)

    os.remove(filename)


@bot.message_handler(func=lambda message: message.text == 'Архив')
# @role_required('HR')
def archive(message):
    chat_id = message.chat.id
    old_reviews = Session().query(Form).join(ReviewPeriod).filter(
        Form.review_period_id == ReviewPeriod.id).filter(ReviewPeriod.is_active == False).all()
    if old_reviews:
        msg, paginator = create_reviews_with_paginator('archive', old_reviews, page=1, n=5)
        bot.send_message(chat_id, msg, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Нет завершенных Review. '
                                  'Вы можете остановить его в разделе "Запуск/остановка Review"')


@bot.callback_query_handler(lambda call: 'archive#' in call.data)
def archive_per_page(call):
    old_reviews = Session().query(Form).join(ReviewPeriod).filter(
        Form.review_period_id == ReviewPeriod.id).filter(ReviewPeriod.is_active == False).all()
    chat_id = call.message.chat.id
    if old_reviews:
        page = call.data.split('#')[-1]
        msg, paginator = create_reviews_with_paginator('archive', old_reviews, page=int(page), n=5)
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=paginator.markup)
    else:
        bot.send_message(chat_id, 'Нет завершенных Review. '
                                  'Вы можете остановить его в разделе "Запуск/остановка Review"')


@bot.callback_query_handler(lambda call: 'archive|rapport' in call.data)
# @role_required('HR')
def get_old_rapport(call):
    pass


@bot.message_handler(commands=['qq'])
# @role_required('HR')
def check_users(message):
    chat_id = message.chat.id
    user = Session().query(User).get(chat_id)
    Session().delete(user)
    Session().commit()
    bot.send_message(chat_id, 'Вы удалены из бота')


@bot.message_handler(commands=['create'])
def create_test_users(message):
    """Create test users"""
    for i in range(11):
        user = Session().query(User).filter_by(id=i).one_or_none()
        if not user:
            user = User(id=i, username=f'username{i}', fullname=f'name{i}', role_id=i % 2)

            dep = Session().query(Department).filter_by(name='Тест').one_or_none()
            user.department_id = dep.id if dep else Department(name='Тест').id
            pos = Session().query(Position).filter_by(name='Тест').one_or_none()
            user.position_id = pos.id if pos else Position(name='Тест').id
            Session().add(user)
            Session().commit()


def init_roles():
    roles = ['Undefined', 'Employee', 'HR', 'Lead']
    for i, role in enumerate(roles):
        role = Role(id=i, name=role)
        Session().add(role)
    Session().commit()


if __name__ == '__main__':
    # init_roles()
    bot.polling()
