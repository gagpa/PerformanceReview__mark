from app.tbot import bot

from app.tbot.storages import ROUTES, COMMANDS


@bot.message_handler(commands=['start'])
def start(call):
    bot.send_message(chat_id=call.message.chat.id, text=call.message.chat.id)


@bot.callback_query_handler(func=lambda call: True or call.data in ROUTES.keys())
def callback_routes(call):
    ROUTES[call.data](message=call.message)


@bot.message_handler(commands=COMMANDS.keys())
def command_routes(message):
    key = message.text.replace('/', '')
    COMMANDS[key](message=message)
