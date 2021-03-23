"""
Файл с конфигами логеера.
"""

import os

from loguru import logger

__LOG_FORMAT = os.environ['LOG_FORMAT']
__LOG_ROTATION = os.environ['LOG_ROTATION']
__LOG_LEVEL = os.environ['LOG_LEVEL']
__LOG_PATH = os.environ['LOG_PATH']


def init_logger_config():
    """ Инициализировать настройки логгера """
    logger.add(f'{__LOG_PATH}/debug.log', format=__LOG_FORMAT, level='DEBUG', rotation=__LOG_ROTATION,
               compression='zip')
    logger.add(f'{__LOG_PATH}/error.log', format=__LOG_FORMAT, level='ERROR', rotation=__LOG_ROTATION,
               compression='zip')
    logger.add(f'{__LOG_PATH}/info.log', format=__LOG_FORMAT, level='INFO', rotation=__LOG_ROTATION,
               compression='zip')
