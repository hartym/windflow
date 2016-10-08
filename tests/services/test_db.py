import pytest
from mock import sentinel
from sqlalchemy.orm import Session
from windflow.services.db import Database


class BaseModelStub():
    @property
    def metadata(self):
        return sentinel.metadata


class MemoryDatabase(Database):
    dsn = 'sqlite://'

    def load(self):
        return BaseModelStub()


def test_missing_dsn():
    class MissingDsnDatabase(Database):
        pass

    with pytest.raises(AttributeError):
        MissingDsnDatabase()


def test_missing_load_impl():
    class MissingLoadImplDatabase(Database):
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
        assert isinstance(session, Session)
