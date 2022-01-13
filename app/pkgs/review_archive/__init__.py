import json
import typing
from urllib.parse import urljoin
from uuid import UUID

import requests

from app.db import Session
from app.models import Form, ReviewPeriod
from app.pkgs.report.frame_creator import create_form_frame
from app.schemas import FormFrame
from app.services.form_review import FormService
from configs.bot_config import ARCHIVE_SERVICE
from .. import exc


class ReviewArchive:

    def archive_form(self, review_id: UUID, form: Form) -> UUID:
        """Заархивировать анкету"""
        request = create_form_frame(form).dict()
        request.update(review=str(review_id))
        response = requests.post(urljoin(ARCHIVE_SERVICE, 'api/v1/form'), json=request)
        if response.status_code == 201:
            return UUID(json.loads(response.content)['data']['id'])
        raise exc.ModuleNotAvliable('archive')

    def archive_review(self, review: ReviewPeriod):
        """Заархивировать review"""
        review_id = self.create_review(review)
        for form in review.forms:
            self.archive_form(review_id, form)
            for project in form.projects:
                for rate in project.ratings:
                    Session().delete(rate)
                Session().commit()
            FormService.delete(form)
        Session().delete(review)
        Session().commit()

    def create_review(self, review: ReviewPeriod) -> UUID:
        """Создать review в архиве"""
        request = \
            {
                'start_date': review.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
                'end_date': review.end_date.strftime('%Y-%m-%dT%H:%M:%S'),

            }
        response = requests.post(urljoin(ARCHIVE_SERVICE, 'api/v1/review_archive'), json=request)
        if response.status_code == 201:
            return UUID(json.loads(response.content)['data']['id'])
        raise exc.ModuleNotAvliable('archive')

    def find_form(self, form_id: UUID) -> FormFrame:
        """Найти анкету в архиве"""
        response = requests.get(urljoin(ARCHIVE_SERVICE, f'api/v1/form/{form_id}'))
        if response.status_code == 200:
            return FormFrame(**json.loads(response.content)['data'])
        raise exc.ModuleNotAvliable('archive')

    def find_review(self, review_id: UUID) -> typing.List[FormFrame]:
        """Найти review в архиве"""
        response = requests.post(urljoin(ARCHIVE_SERVICE, f'api/v1/review_archive/{review_id}'))
        if response.status_code == 200:
            return [FormFrame(**data) for data in json.loads(response.content)['data']]
        raise exc.ModuleNotAvliable('archive')


__all__ = ['ReviewArchive']
