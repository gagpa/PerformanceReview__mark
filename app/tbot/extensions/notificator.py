class Notificator:

    def __init__(self, bot):
        self.bot = bot

    def notificate(self, template, *chat_ids):
        """ Переслать сообщение всем """
        message, markup = template.dump()
        for chat_id in chat_ids:
            self.bot.send_message(chat_id=chat_id, text=message, reply_markup=markup, parse_mode='html')
