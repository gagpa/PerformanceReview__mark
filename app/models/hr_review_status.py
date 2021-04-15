from sqlalchemy import Column, VARCHAR, SmallInteger

from app.db import Base


class HrReviewStatus(Base):
    """ Модель статуса формы """
    __tablename__ = 'hr_review_statuses'
    id = Column(SmallInteger, primary_key=True)

    name = Column(VARCHAR(50), unique=True, nullable=False)

    def __repr__(self):
        return f'HrReviewStatus: {self.name}'


__all__ = ['HrReviewStatus']
