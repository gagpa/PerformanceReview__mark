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
        """ Вернуть summary по pk """
        summary = Session().query(Summary).get(pk)
        return summary

    def by_form_id(self, pk: int) -> Summary:
        """ Вернуть summary по form_id """
        summary = Session().query(Summary).filter_by(form_id=pk).one_or_none()
        return summary


__all__ = ['SummaryService']