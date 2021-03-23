import telebot
from telebot import apihelper

from configs.bot_config import TOKEN

apihelper.ENABLE_MIDDLEWARE = True

#  Создание бота
bot = telebot.TeleBot(TOKEN)

#  Активация Middlewares

from app.tbot.extensions import OrderMiddlewares

OrderMiddlewares().activate()

#  Активация маршрутов обработчиков
from app.tbot import routes


__all__ = ['bot']
