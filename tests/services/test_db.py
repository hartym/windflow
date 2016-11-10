import pytest
from mock import sentinel
from sqlalchemy.orm import scoped_session
from windflow.services.db import Database


class BaseModelStub():
    @property
    def metadata(self):
        return sentinel.metadata


class DatabaseMock(Database):
    engine_factory_options = {}
    sessionmaker_options = {}


class MemoryDatabase(DatabaseMock):
    dsn = 'sqlite://'

    def load(self):
        return BaseModelStub()


def test_missing_dsn():
    class MissingDsnDatabase(DatabaseMock):
        pass

    with pytest.raises(AttributeError):
        MissingDsnDatabase()


def test_missing_load_impl():
    class MissingLoadImplDatabase(DatabaseMock):
        dsn = 'sqlite://'

    with pytest.raises(NotImplementedError):
        MissingLoadImplDatabase()


def test_singletonage():
    db1, db2 = MemoryDatabase(), MemoryDatabase()

    assert db1 is db2
    assert db1.metadata is sentinel.metadata


def test_session_builder():
    db = MemoryDatabase()

    with db() as session:
        assert isinstance(session, scoped_session)
