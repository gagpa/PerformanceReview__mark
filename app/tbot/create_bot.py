import telebot
from telebot import apihelper

from config import config

apihelper.ENABLE_MIDDLEWARE = True

bot = telebot.TeleBot(config.TOKEN)
