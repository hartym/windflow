from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.web import HTTPError
from windmill.services import Service


class Database(Service):
    name = 'database'
    dsn = None

    def __init__(self):
        if not self.dsn:
            raise AttributeError('DSN is required.')
        self.engine = create_engine(self.dsn)
        self.sessionmaker = sessionmaker(bind=self.engine)

    @contextmanager
    def __call__(self):
        from sqlalchemy.orm.exc import NoResultFound
        try:
            yield self.sessionmaker()
        except NoResultFound as e:
            raise HTTPError(404)
