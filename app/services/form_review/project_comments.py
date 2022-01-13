from statistics import mean

from sqlalchemy import or_

from app.db import Session
from app.models import Form, User, Project, CoworkerProjectRating, CoworkerReview
from app.services.abc_entity import Entity
from app.services.form_review import FormService


class ProjectCommentService(Entity):
    """ Сервис комментариев """
    Model = Form

    @classmethod
    def boss_projects_comments(cls, pk):
        """ Комментарии руководителя о проектах формы"""
        form = FormService().by_pk(pk)
        projects_comments = Session().query(CoworkerProjectRating) \
            .join(Project, CoworkerProjectRating.project) \
            .join(Form, Project.form) \
            .join(CoworkerReview, CoworkerReview.id == CoworkerProjectRating.coworker_review_id) \
            .join(User, CoworkerReview.coworker)
        boss_comments = projects_comments \
            .filter(Form.id == form.id) \
            .filter(User.id == form.user.boss_id).all()
        return boss_comments

    @classmethod
    def coworkers_projects_comments(cls, pk):
        """ Комментарии коллег о проектах формы"""
        form = FormService().by_pk(pk)
        projects_comments = Session().query(CoworkerProjectRating) \
            .join(Project, CoworkerProjectRating.project) \
            .join(Form, Project.form) \
            .join(CoworkerReview, CoworkerReview.id == CoworkerProjectRating.coworker_review_id) \
            .join(User, CoworkerReview.coworker)
        coworkers_comments = projects_comments \
            .filter(Form.id == form.id) \
            .filter(User.id != form.user.boss_id) \
            .filter(or_(User.boss_id != form.user_id, User.boss_id == None)).all()
        return coworkers_comments

    @classmethod
    def subordinate_projects_comments(cls, pk):
        """ Комментарии подчиненных о проектах формы"""
        form = FormService().by_pk(pk)
        projects_comments = Session().query(CoworkerProjectRating) \
            .join(Project, CoworkerProjectRating.project) \
            .join(Form, Project.form) \
            .join(CoworkerReview, CoworkerReview.id == CoworkerProjectRating.coworker_review_id) \
            .join(User, CoworkerReview.coworker)
        subordinate_comments = projects_comments.filter(Form.id == form.id) \
            .filter(User.boss_id == form.user.id).all()
        return subordinate_comments

    @classmethod
    def final_rating(cls, pk):
        """ Средняя оценка по проектам формы"""
        all_comments = [
            cls.boss_projects_comments(pk),
            cls.subordinate_projects_comments(pk),
            cls.coworkers_projects_comments(pk),
        ]
        all_ratings = []
        for comments in all_comments:
            if comments:
                rating = []
                for comment in comments:
                    if comment.rating and comment.rating.value > 0:
                        rating.append(comment.rating.value)
                all_ratings.append(mean(rating)) if rating else None

        return round(mean(all_ratings), 2) if all_ratings else None

    @staticmethod
    def project_comments(pk):
        comments = Session().query(CoworkerReview) \
            .join(CoworkerProjectRating, CoworkerReview.projects_ratings) \
            .join(User, CoworkerReview.coworker) \
            .join(Project, CoworkerProjectRating.project) \
            .join(Form, Project.form).filter(Form.id == pk).all()
        return comments
