from app.db import Session
from app.models import Summary
from app.services.abc_entity import Entity


class SummaryService(Entity):
    """ Сущность заключения """
    Model = Summary

    @property
    def all(self):
        """ Вернуть список всех заключений """
        summaries = Session().query(Summary).all()
        return summaries

    def by_id(self, pk: int) -> Summary:
        """ Вернуть оценку по pk """
        summary = Session().query(Summary).get(pk)
        return summary


__all__ = ['SummaryService']