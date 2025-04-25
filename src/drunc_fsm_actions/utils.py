import json
import os
from contextlib import contextmanager

from drunc_core.fsm.exceptions import (
    DotDruncJsonIncorrectFormat,
    DotDruncJsonNotFound,
    InvalidRunType,
)
from drunc_core.utils.utils import expand_path


@contextmanager
def setenv(key, value):
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
    RUN_TYPES = ["PROD", "TEST"]
    if run_type not in RUN_TYPES:
        raise InvalidRunType(
            f"Invalid run type: '{run_type}'. Must be one of {RUN_TYPES}"
        )
    return run_type


def get_dotdrunc_json(path: str = None):
    if path is None:
        path = os.getenv("DOTDRUNC_JSON", "~/.drunc.json")

    try:
        f = open(expand_path(path))
        dotdrunc = json.load(f)
    except FileNotFoundError:
        raise DotDruncJsonNotFound(f"dotdrunc file not found: '{path}'")
    except json.JSONDecodeError as exc:
        raise DotDruncJsonIncorrectFormat(
            f"dotdrunc file is not a valid JSON: '{path}'"
        ) from exc

    expected_keys = [
        "run_registry_configuration",
        "run_number_configuration",
        "elisa_configuration",
    ]

    if not all(key in dotdrunc for key in expected_keys):
        raise DotDruncJsonIncorrectFormat(
            f"dotdrunc file is missing some expected keys: {expected_keys}"
        )

    return dotdrunc
