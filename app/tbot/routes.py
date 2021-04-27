from app.tbot import bot
from app.tbot.extensions import RequestSerializer, MessageManager
from app.tbot.storages import ROUTES, COMMANDS, PERMISSIONS
from app.db import Session


@bot.callback_query_handler(func=lambda call: call.is_exist)
def callback_routes(call):
    message = call.message
    request = RequestSerializer(message=message)
    response = ROUTES[call.url](request=request)
    MessageManager(bot, COMMANDS, ROUTES, PERMISSIONS).handle_response(request, response, call.url, 'callback')
    Session.remove()


@bot.message_handler(func=lambda message: message.is_exist)
def command_routes(message):
    request = RequestSerializer(message=message)
    response = COMMANDS[message.command](request=request)
    MessageManager(bot, COMMANDS, ROUTES, PERMISSIONS).handle_response(request, response, message.command, 'message', )
    Session.remove()
