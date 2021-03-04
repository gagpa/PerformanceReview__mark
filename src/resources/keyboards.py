import telebot
from telegram_bot_pagination import InlineKeyboardPaginator


class MyPaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = '<'
    current_page_label = '-{}-'
    next_page_label = '>'
    last_page_label = '>>'


def create_reply_start_keyboard():
    """Return main keyboard"""
    markup_inline = telebot.types.ReplyKeyboardMarkup()
    user_requests = telebot.types.KeyboardButton(text='Запросы')
    list_users = telebot.types.KeyboardButton(text='Список сотрудников')

    markup_inline.add(user_requests, list_users)
    return markup_inline


def create_inline_keyboard(kind, service_dict):
    """
    Return inline keyboard
    :param kind: type of data
    :param service_dict: key - button text, value - callback name
    """
    markup_inline = []
    for key in service_dict:
        item = telebot.types.InlineKeyboardButton(text=key,
                                                  callback_data='{}|{}'.format(kind, service_dict[
                                                      key]))
        markup_inline.append(item)
    return markup_inline


def create_inline_keyboard_for_user_request(user_id):
    markup_inline = telebot.types.InlineKeyboardMarkup()
    accept = telebot.types.InlineKeyboardButton(text='Принять',
                                                callback_data='{}|add|{}'.format('requests',
                                                                                 user_id))
    delete = telebot.types.InlineKeyboardButton(text='Отклонить',
                                                callback_data='{}|del|{}'.format('requests',
                                                                                 user_id))
    back = telebot.types.InlineKeyboardButton(text='Назад',
                                              callback_data='{}|back|{}'.format('requests',
                                                                                user_id))
    markup_inline.add(accept, delete)
    markup_inline.add(back)
    return markup_inline


def create_inline_keyboard_for_user_list(user_id):
    markup_inline = telebot.types.InlineKeyboardMarkup()
    change = telebot.types.InlineKeyboardButton(text='Редактировать',
                                                callback_data='{}|change|{}'.format('employee',
                                                                                    user_id))
    delete = telebot.types.InlineKeyboardButton(text='Удалить',
                                                callback_data='{}|del|{}'.format('employee',
                                                                                 user_id))
    back = telebot.types.InlineKeyboardButton(text='Назад',
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
    user_info_dict = {i.id: ' - '.join([i.username, i.full_name]) for i in res[page - 1]}
    users_id = dict(enumerate(user_info_dict.keys(), 1))
    inline_keyboard = create_inline_keyboard(kind + '|get', users_id)
    paginator.add_before(*inline_keyboard)
    msg = '\n'.join([f'{i}. {v}' for i, v in enumerate(user_info_dict.values(), 1)])
    return msg, paginator
