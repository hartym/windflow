import functools

from sqlalchemy.orm import Session
from sqlalchemy.sql import ClauseElement


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


def rowmethod(f):
    @functools.wraps(f)
    def method(cls_or_self, session, *args, **kwargs):
        if not isinstance(session, Session):
            raise ValueError('Models and model rows methods must take a session as second argument.')
        return f(cls_or_self, session, *args, **kwargs)

    return method


def modelmethod(f):
    return classmethod(rowmethod(f))
