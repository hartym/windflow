import os

from mock import patch
from windflow.settings import load_settings_from_env


def test_load_settings_from_env(tmpdir):
    with patch.dict('os.environ', {}) as e:
        load_settings_from_env(str(tmpdir))
        assert os.environ.get('FOO', None) is None

    p = tmpdir.join(".env")
    p.write("FOO = bar")

    with patch.dict('os.environ', {}) as e:
        load_settings_from_env(str(tmpdir))
        assert os.environ.get('FOO', None) == 'bar'
