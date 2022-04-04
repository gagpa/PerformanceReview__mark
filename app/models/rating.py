from sqlalchemy import Column, VARCHAR, SmallInteger

from app.db import Base


class Rating(Base):
    """ Модель рейтинга """
    __tablename__ = 'ratings'
    id = Column(SmallInteger, primary_key=True)

    name = Column(VARCHAR(25), nullable=False, unique=True)
    value = Column(SmallInteger, nullable=False, unique=True)

    def __repr__(self):
        return f'Rating {self.name} = {self.value}'


__all__ = ['Rating']
