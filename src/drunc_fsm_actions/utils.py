import json
import os
from contextlib import contextmanager
from pathlib import Path

from drunc_core.fsm.exceptions import (
    DotDruncJsonIncorrectFormat,
    DotDruncJsonNotFound,
    InvalidRunType,
)
from drunc_core.utils.utils import expand_path


@contextmanager
def setenv(key: str, value: str | bool | float) -> None:
    old_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old_value is None:
            del os.environ[key]
        else:
            os.environ[key] = old_value


def validate_run_type(run_type: str) -> str:
    """Validate the run type
    :param run_type: the run type
    :return: the validated run type
    """
    run_types = ["PROD", "TEST"]
    if run_type not in run_types:
        msg = f"Invalid run type: '{run_type}'. Must be one of {run_types}"
        raise InvalidRunType(
            msg,
        )
    return run_type


def get_dotdrunc_json(path: str | None = None) -> dict:
    if path is None:
        path = os.getenv("DOTDRUNC_JSON", "~/.drunc.json")

    try:
        with Path(expand_path(path)).open() as f:
            dotdrunc = json.load(f)
    except FileNotFoundError as exc:
        msg = f"dotdrunc file not found: '{path}'"
        raise DotDruncJsonNotFound(msg) from exc
    except json.JSONDecodeError as exc:
        msg = f"dotdrunc file is not a valid JSON: '{path}'"
        raise DotDruncJsonIncorrectFormat(
            msg,
        ) from exc

    expected_keys = [
        "run_registry_configuration",
        "run_number_configuration",
        "elisa_configuration",
    ]

    if not all(key in dotdrunc for key in expected_keys):
        msg = f"dotdrunc file is missing some expected keys: {expected_keys}"
        raise DotDruncJsonIncorrectFormat(
            msg,
        )

    return dotdrunc
