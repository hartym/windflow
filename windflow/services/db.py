import functools
from contextlib import contextmanager

import sqlalchemy
import sqlalchemy.orm
from windflow.services import Service


class Database(Service):
    """
    SQLAlchemy database service.

    """

    name = 'database'
    dsn = None

    @property
    def metadata(self):
        return self.load().metadata

    def __init__(self):
        if not self.dsn:
            raise AttributeError('DSN is required.')
        self.engine = sqlalchemy.create_engine(self.dsn, connect_args={'connect_timeout': 2})
        self.sessionmaker = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.load()

    def __call__(self):
        """
        :return sqlalchemy.orm.session.Session:
        """
        self.load()
        session = self.sessionmaker()
        try:
            yield session
        finally:
            session.close()

    def with_session(self, f):
        """method decorator that injects the session as first argument."""
        @functools.wraps(f)
        def wrapped_with_session(*args):
            with self() as session:
                return f(args[0], session, *args[1:])

        return wrapped_with_session

    def load(self):
        raise NotImplementedError(
            'You must implement `load()` method on Database service, and return your SQLAlchemy base model.')


Database.__call__ = contextmanager(Database.__call__)

try:
    from alembic import command as alembic_cmd
    from alembic.config import Config as AlembicCfg
except ImportError as e:
    ALEMBIC_NOT_INSTALLED_ERROR = 'AlembicMigrationsMixin requires the optional "alembic" dependency. Install it with `pip install alembic`.'


    def alembic_cmd(*a, **kw):
        raise NotImplementedError(ALEMBIC_NOT_INSTALLED_ERROR)


    def AlembicCfg(*a, **kw):
        raise NotImplementedError(ALEMBIC_NOT_INSTALLED_ERROR)


class DatabaseMigrationsMixin:
    alembic_cfg_path = 'alembic.ini'

    load = Database.load
    metadata = Database.metadata

    @property
    def alembic_cfg(self):
        return AlembicCfg(self.alembic_cfg_path)

    def execute_up(self, logger, options):
        self.load()

        if options.reset:
            self.execute_down(options, logger)

        logger.info('Migrating database...')
        alembic_cmd.upgrade(self.alembic_cfg, "head")

    def execute_down(self, logger, options):
        self.load()

        logger.info('Trying to downgrade database...')
        try:
            alembic_cmd.downgrade(self.alembic_cfg, 'base')
        except Exception as e:
            logger.warning('Error while downgrading: %s', e)

        logger.info('Forcing base revision...')
        try:
            alembic_cmd.stamp(self.alembic_cfg, 'base')
        except Exception as e:
            logger.warning('Error while stamping: %s', e)

        logger.info('Dropping what remains...')
        self.metadata.drop_all(self.engine)

    def register_commands(self, subparsers):
        parser = subparsers.add_parser('db')
        parser.set_defaults(handler=None)

        subparsers = parser.add_subparsers(dest='handler')
        subparsers.required = True

        up = subparsers.add_parser('up')
        up.set_defaults(handler=self.execute_up)
        up.add_argument('--reset', action='store_true', default=False)

        down = subparsers.add_parser('down')
        down.set_defaults(handler=self.execute_down)

        return parser
