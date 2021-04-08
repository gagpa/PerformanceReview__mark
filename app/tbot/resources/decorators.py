from app.db import db_session
from app.models import User
from app.tbot.create_bot import bot


def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            message = args[0]
            user = db_session.query(User).get(message.chat.id)
            if user and (user.role == role):
                func(*args, **kwargs)
            else:
                bot.send_message(message.chat.id, 'Доступ запрещен')

        return wrapper

    return decorator


def check_message(func):
    def wrapper(*args, **kwargs):
        message = args[0]
        if message.text.lower().strip() not in ['отмена', 'список сотрудников', 'запросы',
                                                'запуск/остановка review', 'текущий review']:
            func(*args, **kwargs)
        else:
            bot.send_message(message.chat.id, 'Внесение изменений отменено. Попробуйте снова')

    return wrapper
