import functools

from sqlalchemy.orm import Session, scoped_session
from sqlalchemy.sql import ClauseElement


def get_or_create(session, model, defaults=None, **kwargs):
    """
    :param Session session:
    :param model:
    :param defaults:
    :param kwargs:
    :return:
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


def model_getter_method_with_memory_cache(*filters):
    def model_getter_method_with_memory_cache_decorator(f):
        @functools.wraps(f)
        @classmethod
        def getter(cls, session, *values, create=True, **defaults):
            nonlocal f, filters
            # get or create cache dict
            cache_holder = session or cls
            cache = getattr(cache_holder, '_unique_cache', None)
            if cache is None:
                cache_holder._unique_cache = cache = {}

            filter_values = {}
            for i, (filter, filter_type) in enumerate(filters):
                if not isinstance(values[i], filter_type):
                    filter_values[filter] = filter_type.get(session, values[i], create=create)
                else:
                    filter_values[filter] = values[i]

            key = (cls,) + values
            if not key in cache:
                cache[key] = f(cls, session, filter_values) if session else None
                if cache[key] is None:
                    cache[key] = cls(**filter_values, **defaults) if create else None
                if cache[key] and session:
                    session.add(cache[key])
            return cache[key]

        return getter

    return model_getter_method_with_memory_cache_decorator


class Filter:
    def __init__(self, name, instanceof, factory=None):
        self.name = name
        self.instanceof = instanceof
        self.factory = factory or instanceof

    def __call__(self, session, value, **kwargs):
        try:
            factory = self.factory.apply(self.instanceof, session, create=kwargs.get('create', True))
        except AttributeError as e:
            factory = self.factory
        return factory(value)


def _get_cache_dict(cls, session):
    # use session if provided, fall back on model if not tied to a session.
    cache_holder = session or cls
    if not hasattr(cache_holder, '_unique_cache'):
        cache_holder._unique_cache = {}
    return cache_holder._unique_cache


def _apply_filters(filters, values, create=True, session=None):
    return {
        filter.name: (
            values[i] if isinstance(values[i], filter.instanceof)
            else filter(session, values[i], create=create)
        ) for i, filter in enumerate(filters)
        }


class Getter:
    """
    Flexible decorator to generate model getters.
    """

    def __init__(self, *filters):
        self.filters = list(filters)
        self.getter = None

    def add_filter(self, filter):
        self.filters.append(filter)

    @classmethod
    def mark_as_getter(cls, f):
        f.apply = lambda *args, **kwargs: functools.partial(f, *args, **kwargs)
        return f

    def __wrapped_call__(self, model, session, *values, create=True, **defaults):
        assert session is None or isinstance(session, (
            Session, scoped_session)), 'If provided, session should be an sqlalchemy session object.'

        # cache ?
        cache = _get_cache_dict(model, session)
        cache_key = (model,) + values

        # compute filter values (includes call to related models)
        values = _apply_filters(self.filters, values, create=create, session=session)

        # if no cache, delegate to real (decorated) Getter method
        if not cache_key in cache:
            # wrapped method call
            cache[cache_key] = self.getter(model, session, values) if session else None

            # store cache
            if cache[cache_key] is None:
                cache[cache_key] = model(**values, **defaults) if create else None

            # tie object to session, if available
            if cache[cache_key] and session:
                session.add(cache[cache_key])

        return cache[cache_key]

    def __call__(self, *args, **kwargs):
        if not self.getter:
            assert len(args) == 1 and not len(kwargs)
            actual_getter = args[0]
            self.getter = actual_getter
            self.__name__ = actual_getter.__name__
            return classmethod(functools.wraps(actual_getter)(self))

        return self.__wrapped_call__(*args, **kwargs)

    apply = lambda self, *args, **kwargs: functools.partial(self, *args, **kwargs)

    __repr__ = lambda self: repr(self.getter).replace('<function ', '<{} '.format(
        type(self).__name__)) if self.getter else super().__repr__()


def rowmethod(f):
    @functools.wraps(f)
    def method(cls_or_self, session, *args, **kwargs):
        if not isinstance(session, (Session, scoped_session)):
            raise ValueError('Model methods must take a session as second argument, got {}.'.format(repr(session)))
        return f(cls_or_self, session, *args, **kwargs)

    return method


def modelmethod(f):
    return classmethod(rowmethod(f))
