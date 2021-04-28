from app.db import Session
from app.services.validator import InvalidTypeValidationError, TextValidationError
from app.tbot import bot
from app.tbot.extensions import RequestSerializer, MessageManager
from app.tbot.services.user import get_previous
from app.tbot.storages import ROUTES, COMMANDS, PERMISSIONS


@bot.callback_query_handler(func=lambda call: call.is_exist)
def callback_routes(call):
    message = call.message
    request = RequestSerializer(message=message)
    try:
        response = ROUTES[call.url](request=request)
    except InvalidTypeValidationError:
        step = get_previous(request)
        if step.url_type == 'callback':
            response = ROUTES[step.text](request)
        else:
            response = COMMANDS[step.text](request=request)
    except TextValidationError:
        step = get_previous(request)
        if step.url_type == 'callback':
            response = ROUTES[step.text](request)
        else:
            response = COMMANDS[step.text](request=request)

    MessageManager(bot, COMMANDS, ROUTES, PERMISSIONS).handle_response(request, response, call.url, 'callback')
    Session.remove()


@bot.message_handler(func=lambda message: message.is_exist)
def command_routes(message):
    request = RequestSerializer(message=message)
    try:
        response = COMMANDS[message.command](request=request)
    except InvalidTypeValidationError:
        step = get_previous(request)
        if step.url_type == 'callback':
            response = ROUTES[step.text](request)
        else:
            response = COMMANDS[step.text](request=request)
    except TextValidationError:
        step = get_previous(request)
        if step.url_type == 'callback':
            response = ROUTES[step.text](request)
        else:
            response = COMMANDS[step.text](request=request)
    MessageManager(bot, COMMANDS, ROUTES, PERMISSIONS).handle_response(request, response, message.command, 'message', )
    Session.remove()
