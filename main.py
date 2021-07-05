import os

from dotenv import load_dotenv

from tests.init_mock_data import add_all_mock_data_in_db

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app.tbot import bot
from loguru import logger
from configs.logger_config import init_logger_config
from time import sleep


@logger.catch
def main():
    """ Запустить приложение """
    try:
        add_all_mock_data_in_db()
    except:
        pass
    init_logger_config()
    while True:
        bot.polling()

        try:
            sleep(2)
        except Exception as e:
            logger.error(e)
            sleep(30)


if __name__ == '__main__':
    main()
