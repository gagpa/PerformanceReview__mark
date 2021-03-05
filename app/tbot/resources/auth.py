from app.models.models import User, db_session


def process_name_step(message, bot):
    try:
        chat_id = message.chat.id
        User.update(chat_id, full_name=message.text)
        bot.send_message(chat_id, 'Введите свою должность')
        bot.register_next_step_handler(message, process_position_step, bot)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')


def process_position_step(message, bot):
    try:
        chat_id = message.chat.id
        User.update(chat_id, position=message.text)
        bot.send_message(chat_id, 'Введите свой отдел')
        bot.register_next_step_handler(message, process_department_step, bot)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')


def process_department_step(message, bot):
    try:
        chat_id = message.chat.id
        User.update(chat_id, department=message.text)
        bot.send_message(chat_id, 'Введите логин руководителя в телеграмм @login или введите "Нет"')
        bot.register_next_step_handler(message, process_chef_step, bot)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')


def process_chef_step(message, bot):
    try:
        chat_id = message.chat.id
        User.update(chat_id, chef=message.text)
        db_session.commit()
        bot.send_message(chat_id, 'Спасибо. Ожидайте разрешения доступа. Вам поступит сообщение.')
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так')
