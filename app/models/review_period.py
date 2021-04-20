from sqlalchemy import Column, Integer, TIMESTAMP, Boolean

from app.db import Base


class ReviewPeriod(Base):
    """ Модель периода review """
    __tablename__ = 'review_periods'
    id = Column(Integer, primary_key=True)

    is_active = Column(Boolean, default=False, nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return f'Review period {self.start_date} - {self.end_date}'


__all__ = ['ReviewPeriod']
