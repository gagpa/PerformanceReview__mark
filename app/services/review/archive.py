from configs.bot_config import ARCHIVE_SERVICE
from urllib.parse import urljoin
import requests
from app.services.exceptions import ModuleNotAvliable
import json


def get_reviews():
    response = requests.get(urljoin(ARCHIVE_SERVICE, 'api/v1/review_archive'))
    if response.status_code != 200:
        raise ModuleNotAvliable
    return json.loads(response.content)['data']


def get_review(review_id):
    response = requests.get(urljoin(ARCHIVE_SERVICE, f'api/v1/review_archive/{review_id}'))
    if response.status_code != 200:
        raise ModuleNotAvliable
    return json.loads(response.content)['data']


def get_form(form_id):
    response = requests.get(urljoin(ARCHIVE_SERVICE, f'api/v1/form/{form_id}'))
    if response.status_code != 200:
        raise ModuleNotAvliable
    return json.loads(response.content)['data']


def get_last():
    return get_review(get_reviews()['items'][-1]['id'])
