from app.db import Session
from app.models import CoworkerAdvice, CoworkerProjectRating, CoworkerReview, Form
from app.services.dictinary import HrReviewStatusService, StatusService, RoleService
from app.services.review import HrReviewService, CoworkerReviewService, ReviewPeriodService
from app.services.user.user import UserService


class HRService(UserService):
    """ Сервис сотрудника """

    def comment_on(self, model, text):
        """ Добавить комментарий """
        model.hr_comment = text
        self.save_all(model)

    def comment_rating(self, pk: int, text: str):
        """ Прокомментировать оценку """
        rating = Session.query(CoworkerProjectRating).filter_by(id=pk).first()
        rating.hr_comment = text
        self.save_all(rating)

    def accept_coworker_review(self, review_pk: int):
        """ Принять комменатрии коллеги """
        service = HrReviewService()
        review = service.by_pk(review_pk)
        review.hr_status = HrReviewStatusService().accept
        form_status = StatusService().accepted
        self.save_all(review)
        if service.is_last_review(review):
            review.form.status = form_status
            self.save_all(review)
        return review

    def decline_coworker_review(self, review_pk: int):
        """ Отклонить комменатрии коллеги """
        review = CoworkerReviewService().by_pk(review_pk)
        hr_status = HrReviewStatusService().coworker
        review.hr_status = hr_status
        self.save_all(review)
        Session.commit()

    def reviews(self):
        form_status = StatusService().coworker_review
        hr_status = HrReviewStatusService().hr
        period = ReviewPeriodService().current
        query = Session.query(CoworkerReview).join(Form)
        query = query.filter(CoworkerReview.hr_status == hr_status,
                             Form.status == form_status,
                             Form.review_period == period)
        reviews = query.all()
        return reviews

    def all(self):
        return self.all_by(role=RoleService().hr)


__all__ = ['HRService']
