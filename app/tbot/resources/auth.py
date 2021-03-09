from app.models.models import User, db_session
from app.tbot.create_bot import bot
from app.tbot.resources.keyboards import create_reply_start_keyboard


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    if not User.lookup(message.chat.id):
        bot.send_message(chat_id,
                         'Приветствую @{}.'.format(message.chat.username))
        user = User(id=chat_id, username=f'@{message.chat.username}')
        db_session.add(user)
        bot.send_message(chat_id, 'Введите свое ФИО')
        bot.register_next_step_handler(message, process_name_step)
    else:
        bot.send_message(chat_id, 'Что бы вы хотели сделать?',
                         reply_markup=create_reply_start_keyboard())


def process_name_step(message):
    try:
        chat_id = message.chat.id
        User.update(chat_id, full_name=message.text)
        bot.send_message(chat_id, 'Введите свою должность')
        bot.register_next_step_handler(message, process_position_step)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')


def process_position_step(message):
    try:
        chat_id = message.chat.id
        User.update(chat_id, position=message.text)
        bot.send_message(chat_id, 'Введите свой отдел')
        bot.register_next_step_handler(message, process_department_step)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')


def process_department_step(message):
    try:
        chat_id = message.chat.id
        User.update(chat_id, department=message.text)
        bot.send_message(chat_id,
                         'Введите логин руководителя в телеграмм @login или введите "Нет"')
        bot.register_next_step_handler(message, process_chef_step)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')


def process_chef_step(message):
    try:
        chat_id = message.chat.id
        User.update(chat_id, chef=message.text)
        db_session.commit()
        bot.send_message(chat_id, 'Спасибо. Ожидайте разрешения доступа. Вам поступит сообщение.')
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')
