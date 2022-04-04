import telebot
from telebot import apihelper

from app.tbot.extensions.notificator import Notificator
from configs.bot_config import TOKEN

apihelper.ENABLE_MIDDLEWARE = True
#  Создание бота
bot = telebot.TeleBot(TOKEN)
notificator = Notificator(bot)

#  Активация Middlewares

from app.tbot.extensions.middlewares import OrderMiddlewares
from app.tbot.middlewares import ORDER_CALLBACK_QUERY_MIDDLEWARES
from app.tbot.middlewares import ORDER_MESSAGE_MIDDLEWARES

OrderMiddlewares(bot, ORDER_MESSAGE_MIDDLEWARES, ORDER_CALLBACK_QUERY_MIDDLEWARES).activate()

#  Активация маршрутов обработчиков
from app.tbot import routes

__all__ = ['bot', 'notificator']
