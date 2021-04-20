from statistics import mean

from app.db import Session
from app.models import Form, User, ProjectComment, Project
from app.services.abc_entity import Entity
from app.services.form_review import FormService


class ProjectCommentService(Entity):
    """ Сервис комментариев """
    Model = Form

    @staticmethod
    def boss_projects_comments(pk):
        """ Комментарии руководителя о проектах формы"""
        form = FormService().by_pk(pk)
        projects_comments = Session().query(ProjectComment) \
            .join(Project, ProjectComment.project) \
            .join(Form, Project.form).join(User, Form.user)
        boss_comments = projects_comments \
            .filter(Form.id == form.id) \
            .filter(ProjectComment.user_id == form.user.boss_id).all()
        return boss_comments

    @staticmethod
    def coworkers_projects_comments(pk):
        """ Комментарии коллег о проектах формы"""
        form = FormService().by_pk(pk)
        projects_comments = Session().query(ProjectComment) \
            .join(Project, ProjectComment.project) \
            .join(Form, Project.form).join(User, Form.user)
        coworkers_comments = projects_comments \
            .filter(Form.id == form.id) \
            .filter(User.boss_id == form.user.boss_id).all()
        return coworkers_comments

    @staticmethod
    def subordinate_projects_comments(pk):
        """ Комментарии подчиненных о проектах формы"""
        form = FormService().by_pk(pk)
        projects_comments = Session().query(ProjectComment) \
            .join(Project, ProjectComment.project) \
            .join(Form, Project.form).join(User, Form.user)
        subordinate_comments = projects_comments.filter(Form.id == form.id) \
            .filter(User.boss_id == form.user.id).all()
        return subordinate_comments

    def final_rating(self, pk):
        """ Средняя оценка по проектам формы"""
        all_ratings = []
        if self.boss_projects_comments(pk):
            boss_rating = [comment.rating.value for comment in self.boss_projects_comments(pk)]
            all_ratings.append(mean(boss_rating))

        if self.coworkers_projects_comments(pk):
            coworkers_rating = [comment.rating.value for comment in
                                self.coworkers_projects_comments(pk)]
            all_ratings.append(mean(coworkers_rating))

        if self.subordinate_projects_comments(pk):
            subordinate_rating = [comment.rating.value for comment in
                                  self.subordinate_projects_comments(pk)]
            all_ratings.append(mean(subordinate_rating))

        return mean(all_ratings)
