import json
from urllib.parse import urljoin

import requests

from app.db import Session
from app.models import ReviewPeriod
from app.services.abc_entity import Entity
from app.services.exceptions import ModuleNotAvliable
from configs.bot_config import ARCHIVE_SERVICE


class ReviewPeriodService(Entity):
    """"""
    Model = ReviewPeriod

    @property
    def current(self) -> ReviewPeriod:
        """ Выдать текущий review период """
        return self.by(is_active=True)

    @property
    def is_now(self) -> bool:
        """ Ответить проходит сейчас ревью """
        return self.is_exist(is_active=True)

    def send_to_archive(self):
        """Отправить Review в архив"""
        request = \
            {
                'start_date': self.model.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
                'end_date': self.model.end_date.strftime('%Y-%m-%dT%H:%M:%S')
            }
        response = requests.post(urljoin(ARCHIVE_SERVICE, 'api/v1/review_archive'), json=request)
        if response.status_code != 201:
            raise ModuleNotAvliable('archive')
        archive_review = json.loads(response.content)['data']['id']
        for form in self.model.forms:
            response = requests.post(urljoin(ARCHIVE_SERVICE, 'api/v1/form'), json=request)
            if response.status_code != 201:
                raise ModuleNotAvliable
            for project in form.projects:
                for rate in project.ratings:
                    Session().delete(rate)
                Session().commit()
            Session().delete(form)
            Session().commit()
        Session().delete(self.model)
        Session().commit()


__all__ = ['ReviewPeriodService']
