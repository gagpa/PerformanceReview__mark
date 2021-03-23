from typing import Optional

from app.db import db_session
from app.models import BossReview, Form
from app.services.status import change_fill_form


def save(model):
    """ Сохранить в БД """
    db_session.add(model)
    db_session.commit()


def is_exist(form: Form) -> bool:
    answer = db_session.query(db_session.query(BossReview).filter(BossReview.form == form).exists()).scalar()
    return answer


def add(form: Form, boss, text: Optional[str] = None) -> BossReview:
    """ Добавить review """
    if is_exist(form):
        review = db_session.query(BossReview).filter_by(form=form).first()
        review.boss = boss
        review.text = text
    else:
        review = BossReview(form=form, boss=boss, text=text)
    save(review)
    print(form.status)
    change_fill_form(form)
    print(form.status)
    return review
