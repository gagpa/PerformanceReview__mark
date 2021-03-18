import telebot

from configs.bot_config import TOKEN
from telebot import apihelper

apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(TOKEN)

from app.tbot import middlewares
from app.tbot import routes
