import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app.tbot import bot
from loguru import logger
from configs.logger_config import init_logger_config
from tests.init_mock_data import add_all_mock_data_in_db


@logger.catch
def main():
    """ Запустить приложение """
    #add_all_mock_data_in_db()
    init_logger_config()
    bot.polling()


if __name__ == '__main__':
    main()
