import datetime

import telebot_calendar
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator

from app.tbot.create_bot import bot


class MyPaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = '<'
    current_page_label = '-{}-'
    next_page_label = '>'
    last_page_label = '>>'


def create_reply_start_keyboard():
    """Return main keyboard"""
    markup_inline = ReplyKeyboardMarkup()
    user_requests = KeyboardButton(text='Запросы')
    list_users = KeyboardButton(text='Список сотрудников')
    review = KeyboardButton(text='Запуск/остановка Review')
    current_review = KeyboardButton(text='Текущий Review')

    markup_inline.add(user_requests, list_users, review, current_review)
    return markup_inline


def create_inline_keyboard(kind, service_dict):
    """
    Return inline keyboard
    :param kind: type of data
    :param service_dict: key - button text, value - callback name
    """
    buttons = []
    for key in service_dict:
        item = InlineKeyboardButton(text=key,
                                    callback_data='{}|{}'.format(kind, service_dict[key]))
        buttons.append(item)
    if 'get' in kind or 'rapport' in kind:
        return buttons
    else:
        markup_inline = InlineKeyboardMarkup()
        markup_inline.add(*buttons)
        return markup_inline


def create_inline_keyboard_for_user_request(user_id):
    markup_inline = InlineKeyboardMarkup()
    accept = InlineKeyboardButton(text='Принять',
                                  callback_data='{}|add|{}'.format('requests',
                                                                   user_id))
    delete = InlineKeyboardButton(text='Отклонить',
                                  callback_data='{}|del|{}'.format('requests',
                                                                   user_id))
    back = InlineKeyboardButton(text='Назад',
                                callback_data='{}|back|{}'.format('requests',
                                                                  user_id))
    markup_inline.add(accept, delete)
    markup_inline.add(back)
    return markup_inline


def create_inline_keyboard_for_user_list(user_id):
    markup_inline = InlineKeyboardMarkup()
    change = InlineKeyboardButton(text='Редактировать',
                                  callback_data='{}|change|{}'.format('employee',
                                                                      user_id))
    delete = InlineKeyboardButton(text='Удалить',
                                  callback_data='{}|del|{}'.format('employee',
                                                                   user_id))
    back = InlineKeyboardButton(text='Назад',
                                callback_data='{}|back|{}'.format('employee',
                                                                  user_id))
    markup_inline.add(change, delete)
    markup_inline.add(back)
    return markup_inline


def create_users_with_paginator(kind, users, page=1, n=5):
    res = [users[i:i + n] for i in range(0, len(users), n)]
    paginator = MyPaginator(
        len(res),
        current_page=page,
        data_pattern=kind + '#{page}'
    )
    user_info_dict = {i.id: ' - '.join([i.username, i.fullname]) for i in res[page - 1]}
    users_id = dict(enumerate(user_info_dict.keys(), 1))
    inline_keyboard = create_inline_keyboard(kind + '|get', users_id)
    paginator.add_before(*inline_keyboard)
    msg = '\n'.join([f'{i}. {v}' for i, v in enumerate(user_info_dict.values(), 1)])
    return msg, paginator


def create_reviews_with_paginator(kind, review, page=1, n=5):
    res = [review[i:i + n] for i in range(0, len(review), n)]
    paginator = MyPaginator(
        len(res),
        current_page=page,
        data_pattern=kind + '#{page}'
    )
    user_info_dict = {i.id: ' - '.join([i.user.fullname, i.status.name]) for i in res[page - 1]}
    users_id = dict(enumerate(user_info_dict.keys(), 1))
    inline_keyboard = create_inline_keyboard(kind + '|rapport', users_id)
    paginator.add_before(*inline_keyboard)
    msg = '\n'.join([f'{i}. {v}' for i, v in enumerate(user_info_dict.values(), 1)])
    return msg, paginator


def create_archive_with_paginator(kind, forms, page=1, n=5):
    res = [forms[i:i + n] for i in range(0, len(forms), n)]
    paginator = MyPaginator(
        len(res),
        current_page=page,
        data_pattern=kind + '#{page}'
    )
    user_info_dict = {i.id: ' - '.join([i.user.fullname, i.status.name]) for i in res[page - 1]}
    users_id = dict(enumerate(user_info_dict.keys(), 1))
    inline_keyboard = create_inline_keyboard(kind + '|rapport', users_id)
    paginator.add_before(*inline_keyboard)
    msg = '\n'.join([f'{i}. {v}' for i, v in enumerate(user_info_dict.values(), 1)])
    return msg, paginator


def choose_date(chat_id, call_data, msg):
    now = datetime.datetime.now()
    # документация по календарю: https://github.com/FlymeDllVa/telebot-calendar
    calendar = telebot_calendar.CallbackData(call_data, "action", "year", "month", "day")
    bot.send_message(chat_id, msg,
                     reply_markup=telebot_calendar.create_calendar(name=calendar.prefix,
                                                                   year=now.year,
                                                                   month=now.month))
