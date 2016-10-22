from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declared_attr
from windflow.models.utils import modelmethod


class TimestampableMixin():
    created_at = Column('created_at', DateTime, default=func.now())
    '''Row insertion timestamp.'''

    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    '''Row update timestamp.'''


class TextDimensionMixin(TimestampableMixin):
    '''
    Generic model mixin used to build text dimension models.
    '''
    id = Column(Integer, primary_key=True)
    '''Primary key.'''

    value = Column(String, unique=True)
    '''Dimension value.'''

    @declared_attr
    def __tablename__(cls):
        return 'dim_' + cls.__name__.lower()

    @modelmethod
    def get(cls, session, value, mock=False):
        obj = ((not mock) and session.query(cls).filter_by(value=value).first()) or cls(value=value)
        if session:
            session.add(obj)
        return obj

    def __str__(self):
        return self.value
