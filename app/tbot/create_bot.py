import telebot
from telebot import apihelper

from configs.bot_config import TOKEN

apihelper.ENABLE_MIDDLEWARE = True

bot = telebot.TeleBot(TOKEN)
