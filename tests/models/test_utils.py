import pytest
from sqlalchemy.orm.session import Session
from windflow.models.utils import modelmethod, rowmethod


class ModelStub:
    @modelmethod
    def my_model_method(cls, sess, a):
        return cls, sess, a

    @rowmethod
    def my_row_method(self, sess, a):
        return self, sess, a


def test_modelmethod():
    session = Session()

    with pytest.raises(ValueError) as e:
        ModelStub.my_model_method(1, 2)

    c, s, a = ModelStub.my_model_method(session, 1)

    assert c is ModelStub
    assert s is session
    assert a == 1


def test_rowmethod():
    session = Session()

    with pytest.raises(ValueError) as e:
        ModelStub.my_row_method(0, 1, 2)

    c, s, a = ModelStub.my_row_method(0, session, 1)

    assert c is 0
    assert s is session
    assert a == 1

    i = ModelStub()

    c, s, a = i.my_row_method(session, 2)
    assert c is i
    assert s is session
    assert a == 2
