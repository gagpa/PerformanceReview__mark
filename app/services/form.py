from app.db import db_session
from app.models import Form, User, ReviewPeriod, Status, Rating
from app.services.status import STATUS_BOSS_REVIEW, STATUS_COWORKER_REVIEW


def is_exist(user: User, review_period: ReviewPeriod) -> bool:
    """ Проверка существование формы """
    answer = db_session.query(db_session.query(Form).
                              filter_by(user=user, review_period=review_period).
                              exists()).scalar()
    return answer


def save(form: Form):
    """ Сохранить """
    db_session.add(form)
    db_session.commit()


def create(user: User, review_period: ReviewPeriod, status: Status, rating: Rating = None):
    """ Создание формы """
    form = Form(user=user, review_period=review_period, status=status)
    save(form)
    return form


def update_status(form: Form, status: Status):
    """ Обновить статус формы """
    form.status = status
    save(form)


def get(user, review_period: ReviewPeriod) -> Form:
    """ Вернуть форму """
    form = db_session.query(Form).filter_by(user=user).first()
    return form


def get_on_boss_review(user, review_period: ReviewPeriod):
    """ Вернуть форму на проверке у начальника """
    status = STATUS_BOSS_REVIEW
    data = db_session.query(Form, User, ReviewPeriod, Status).\
        filter_by(user=user, review_period=review_period, status=status).first()
    if data:
        return data[0]


def get_on_coworker_review(user, review_period: ReviewPeriod):
    """ Вернуть форму на проверке у сотрудника """
    status = STATUS_COWORKER_REVIEW
    data = db_session.query(Form, User, ReviewPeriod, Status).\
        filter_by(user=user, review_period=review_period, status=status).first()
    if data:
        return data[0]


def get_by_id(pk: int):
    """ Вернуть форму по pk """
    form = db_session.query(Form).filter_by(id=pk).first()
    return form
