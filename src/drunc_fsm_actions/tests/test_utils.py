import json
import os
import tempfile

import pytest
from drunc_core.exceptions import DruncException
from drunc_core.fsm.exceptions import DotDruncJsonIncorrectFormat, DotDruncJsonNotFound

from drunc_fsm_actions.utils import get_dotdrunc_json, setenv, validate_run_type


def test_setenv():
    with setenv("SOME_ENV_VAR", "bla"):
        assert os.getenv("SOME_ENV_VAR") == "bla"

        with setenv("SOME_ENV_VAR", "bla2"):
            assert os.getenv("SOME_ENV_VAR") == "bla2"

        assert os.getenv("SOME_ENV_VAR") == "bla"

    assert os.getenv("SOME_ENV_VAR") is None


def test_get_dotdrunc_json(dotdrunc_data):
    with tempfile.NamedTemporaryFile(delete=True, mode="w") as f:
        f.write(json.dumps(dotdrunc_data))
        f.flush()

        dotdrunc = get_dotdrunc_json(f.name)
        assert dotdrunc is not None

        with setenv("DOTDRUNC_JSON", f.name):
            dotdrunc = get_dotdrunc_json()
            assert dotdrunc is not None

        with setenv("DOTDRUNC_JSON", "nonexistent_path"):
            with pytest.raises(DotDruncJsonNotFound):
                get_dotdrunc_json()

    if os.path.exists(os.path.expanduser("~/.drunc.json")):
        dotdrunc = get_dotdrunc_json()
        assert dotdrunc is not None

    with pytest.raises(DotDruncJsonNotFound):
        get_dotdrunc_json("nonexistent_path")

    with tempfile.NamedTemporaryFile(delete=True, mode="w") as f:
        f.write('{"test": "test"}')
        f.flush()

        with pytest.raises(DotDruncJsonIncorrectFormat):
            get_dotdrunc_json(f.name)


def test_validate_run_type():
    assert validate_run_type("PROD") == "PROD"
    assert validate_run_type("TEST") == "TEST"
    with pytest.raises(DruncException):
        validate_run_type("INVALID")
