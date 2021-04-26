from telebot.apihelper import ApiTelegramException
from loguru import logger


class Notificator:

    def __init__(self, bot):
        self.bot = bot

    def notificate(self, template, *chat_ids):
        """ Переслать сообщение всем """
        message, markup = template.dump()
        for chat_id in chat_ids:
            try:
                self.bot.send_message(chat_id=chat_id, text=message, reply_markup=markup, parse_mode='html')
            except ApiTelegramException:
                logger.error(f'Пользователю с chat_id: {chat_id} нельзя отправить сообщение, т.к. его не т в БД')
