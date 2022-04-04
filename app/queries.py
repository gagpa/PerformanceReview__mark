from sqlalchemy import or_

from app import models as m
from app.db import Session


def find__lead_marks(form: m.Form):
    return Session().query(m.CoworkerProjectRating) \
        .join(m.Project, m.CoworkerProjectRating.project) \
        .join(m.Form, m.Project.form) \
        .join(m.CoworkerReview, m.CoworkerReview.id == m.CoworkerProjectRating.coworker_review_id) \
        .join(m.User, m.CoworkerReview.coworker).filter(m.Form.id == form.id) \
        .filter(m.Form.id == form.id) \
        .filter(m.User.id == form.user.boss_id)


def find__coworkers_marks(form: m.Form):
    return Session().query(m.CoworkerProjectRating) \
        .join(m.Project, m.CoworkerProjectRating.project) \
        .join(m.Form, m.Project.form) \
        .join(m.CoworkerReview, m.CoworkerReview.id == m.CoworkerProjectRating.coworker_review_id) \
        .join(m.User, m.CoworkerReview.coworker) \
        .filter(m.Form.id == form.id) \
        .filter(m.User.id != form.user.boss_id) \
        .filter(or_(m.User.boss_id != form.user_id, m.User.boss_id == None))


def find__subordinates_marks(form: m.Form):
    return Session().query(m.CoworkerProjectRating) \
        .join(m.Project, m.CoworkerProjectRating.project) \
        .join(m.Form, m.Project.form) \
        .join(m.CoworkerReview, m.CoworkerReview.id == m.CoworkerProjectRating.coworker_review_id) \
        .join(m.User, m.CoworkerReview.coworker) \
        .filter(m.Form.id == form.id) \
        .filter(m.User.boss_id == form.user.id)
