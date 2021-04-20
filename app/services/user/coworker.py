from app.db import Session
from app.models import Form, Rating, ProjectComment, Project, User, CoworkerAdvice
from app.services.dictinary import StatusService
from app.services.review import ReviewPeriodService, CoworkerReviewService
from app.services.user.user import UserService


class CoworkerService(UserService):
    """ Сервис коллеги """

    def send_hr(self, form):
        """ Отправить HR """
        pass

    def give_todo(self, text, form):
        """ Дать совет что делать"""
        service = CoworkerReviewService(todo=text, form=form, coworker=self.model)
        if service.is_exist(form=form, coworker=self.model):
            service.by(form=form, coworker=self.model)
            service.update(todo=text)
        else:
            service.create(todo=text, form=form, coworker=self.model)

    def give_not_todo(self, text, form):
        """ Дать совет что перестать делать"""
        service = CoworkerReviewService(todo=text, form=form, coworker=self.model)
        if service.is_exist(form=form, coworker=self.model):
            service.by(form=form, coworker=self.model)
            service.update(not_todo=text)
        else:
            service.create(not_todo=text, form=form, coworker=self.model)

    def comment_on(self, text, project):
        """ Прокомментировать проект """
        comment = Session().query(ProjectComment).filter_by(project=project, user=self.model).first()
        comment.text = text
        self.save(comment)

    def find_advice(self, form):
        """ Найти совет """
        advice = Session().query(CoworkerAdvice).filter_by(form=form, coworker=self.model).first()
        return advice

    def find_project_to_comment(self, form: Form) -> list:
        """ Найти проекты в форме для комментирования """
        projects_in_form = form.projects
        projects_to_comment = list(filter(lambda project: self.model in project.users, projects_in_form))
        return projects_to_comment

    def find_right_left_project(self, project):  # TODO Переделать алгортим
        """ """
        projects = self.find_project_to_comment(form=project.form)
        left_project = None
        right_project = None
        if len(projects) > 1:
            index = projects.index(project)
            if index + 1 == len(projects):
                left_project = projects[index - 1]
            elif index == 0:
                right_project = projects[1]
            else:
                left_project = projects[index - 1]
                right_project = projects[index + 1]
        return left_project, right_project

    def find_rating(self, project: Project):
        """ """
        project_comment = Session().query(ProjectComment).filter_by(project=project, user=self.model).first()
        return project_comment.rating

    def find_comment(self, project: Project):
        """ """
        project_comment = Session().query(ProjectComment).filter_by(project=project, user=self.model).first()
        return project_comment

    def rate_project(self, project: Project, rating: Rating):
        """ Оценить проект """
        project_comment = Session().query(ProjectComment).filter_by(project=project, user=self.model).first()
        project_comment.rating = rating
        self.save(project_comment)
        Session.commit()

    @property
    def forms_on_review(self):
        """ Верунть формы на review """
        review_period = ReviewPeriodService().current
        status = StatusService().coworker_review
        query = Session.query(Form)
        query = query.join(Project, Project.form_id == Form.id)
        query = query.join(ProjectComment, ProjectComment.project_id == Project.id)
        query = query.join(User, User.id == ProjectComment.user_id)
        query = query.filter(Form.review_period == review_period,
                             Form.status == status,
                             ProjectComment.user == self.model)
        forms = query.all()
        return forms


__all__ = ['CoworkerService']
