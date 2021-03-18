"""
Файл с конфигами логеера.
"""

import os

from loguru import logger

__LOG_FORMAT = os.environ['LOG_FORMAT']
__LOG_ROTATION = os.environ['LOG_ROTATION']
__LOG_LEVEL = os.environ['LOG_LEVEL']
__LOG_PATH = os.environ['LOG_PATH']
logger.add('logs/debug.log', format=__LOG_FORMAT, level='DEBUG', rotation=__LOG_ROTATION, compression='zip')
logger.add('logs/error.log', format=__LOG_FORMAT, level='ERROR', rotation=__LOG_ROTATION, compression='zip')
logger.add('logs/info.log', format=__LOG_FORMAT, level='INFO', rotation=__LOG_ROTATION, compression='zip')
