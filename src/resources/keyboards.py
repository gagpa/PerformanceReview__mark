import telebot


def create_reply_start_keyboard():
    markup_inline = telebot.types.ReplyKeyboardMarkup()
    user_requests = telebot.types.KeyboardButton(text='Запросы')
    list_users = telebot.types.KeyboardButton(text='Список сотрудников')

    markup_inline.add(user_requests, list_users)
    return markup_inline


def create_inline_keyboard(kind, service_dict):
    markup_inline = telebot.types.InlineKeyboardMarkup()
    for key in service_dict:
        item = telebot.types.InlineKeyboardButton(text=key,
                                                  callback_data='{}|get|{}'.format(kind, service_dict[key]))
        markup_inline.add(item)
    return markup_inline


def create_inline_keyboard_for_user_request(user_id):
    markup_inline = telebot.types.InlineKeyboardMarkup()
    accept = telebot.types.InlineKeyboardButton(text='Принять',
                                                callback_data='{}|add|{}'.format('requests', user_id))
    delete = telebot.types.InlineKeyboardButton(text='Отклонить',
                                                callback_data='{}|del|{}'.format('requests', user_id))
    back = telebot.types.InlineKeyboardButton(text='Назад',
                                              callback_data='{}|back|{}'.format('requests', user_id))
    markup_inline.add(accept, delete)
    markup_inline.add(back)
    return markup_inline
