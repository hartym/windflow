from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declared_attr
from windflow.models.utils import Filter, Getter
from windflow.utils import generate_repr_method, generate_str_method


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

    @Getter(Filter('value', str))
    def get(cls, session, filters):
        return session.query(cls).filter_by(**filters).first()

    __str__ = generate_str_method('value')
    __repr__ = generate_repr_method('value')
