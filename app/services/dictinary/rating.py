from typing import List

from app.db import Session
from app.models import Rating
from app.services.abc_entity import Entity


class RatingService(Entity):
    """ Сущность оценки """
    Model = Rating

    @property
    def all(self) -> List[Rating]:
        """ Вернуть список всех рейтингов """
        ratings = Session().query(Rating).all()
        return ratings

    def by_id(self, pk: int) -> Rating:
        """ Вернуть оценку по pk """
        rating = Session().query(Rating).get(pk)
        return rating


__all__ = ['RatingService']
