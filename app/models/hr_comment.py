from sqlalchemy import Column, VARCHAR, SmallInteger

from app.db import Base


class HrComment(Base):
    """ Модель статуса формы """
    __tablename__ = 'hr_comments'
    id = Column(SmallInteger, primary_key=True)

    text = Column(VARCHAR(1000), nullable=False)

    def __repr__(self):
        return f'HrComment: {self.text}'


__all__ = ['HrComment']
