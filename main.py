import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app.tbot import bot
from loguru import logger
from configs.logger_config import init_logger_config


@logger.catch
def main():
    """ Запустить приложение """
    init_logger_config()
    bot.polling()


if __name__ == '__main__':
    main()
