"""
Файл с конфигами БД.
"""

import os


class DbEnvNotFound(KeyError):
    pass


#  Движок для PSQL. Если используется другая база, то можно изменить.
DB_ENGINE = 'postgresql+psycopg2'
try:
    DB_USER = os.environ['SQL_USER']
    DB_PASS = os.environ['SQL_PASS']
    DB_HOST = os.environ['SQL_HOST']
    DB_PORT = os.environ['SQL_PORT']
    DB_NAME = os.environ['SQL_DBNAME']
except KeyError:
    raise DbEnvNotFound

DATABASE_URI = f'{DB_ENGINE}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
