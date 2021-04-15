from app.db import Session
from app.models import User, Department, Position, Role
from app.tbot import bot


def process_name_step(message, user):
    try:
        chat_id = message.chat.id
        user.fullname = message.text
        bot.send_message(chat_id, 'Введите свою должность')
        bot.register_next_step_handler(message, process_position_step, user)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Что-то пошло не так')


def process_position_step(message, user):
    try:
        chat_id = message.chat.id
        user.position = Position(name=message.text)
        bot.send_message(chat_id, 'Введите свой отдел')
        bot.register_next_step_handler(message, process_department_step, user)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Что-то пошло не так')


def process_department_step(message, user):
    try:
        chat_id = message.chat.id
        user.department = Department(name=message.text)
        bot.send_message(chat_id,
                         'Введите логин руководителя в телеграмм @login или введите "Нет"')
        bot.register_next_step_handler(message, process_chef_step, user)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Что-то пошло не так')


def process_chef_step(message, user):
    try:
        chat_id = message.chat.id
        boss_login = message.text.lower().replace('@', '')
        if boss_login != 'нет':
            boss = Session().query(User).filter_by(username=boss_login).one_or_none()
            if boss:
                user.boss = boss
            else:
                bot.send_message(chat_id, 'Вашего руководителя еще нет в системе')
        else:
            user.bose = None
        user.role = Session().query(Role).get(0)
        Session().add(user)
        Session().commit()
        bot.send_message(chat_id, 'Спасибо. Ожидайте разрешения доступа. Вам поступит сообщение.')
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Что-то пошло не так')
