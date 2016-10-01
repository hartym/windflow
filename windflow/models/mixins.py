from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declared_attr
from windflow.models.utils import get_or_create


class TimestampableMixin():
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())


class TextDimensionMixin(TimestampableMixin):
    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True)

    @declared_attr
    def __tablename__(cls):
        return 'dim_' + cls.__name__.lower()

    @classmethod
    def get_or_create(cls, session, value):
        return get_or_create(session, cls, value=value)

    def __str__(self):
        return self.value
