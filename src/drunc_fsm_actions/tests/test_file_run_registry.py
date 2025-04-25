import os

from drunc_fsm_actions.file_run_registry import FileRunRegistry

from .conftest import MockController


def test_file_run_registry(dotdrunc_file):
    file_run_registry = FileRunRegistry(
        configuration=None,
        _dry_run=True,
    )
    input_data = {
        "run": 1234,
        "production_vs_test": "TEST",
    }
    context = MockController()
    kwargs = {"some stuff": 123, "some other stuff": 456}
    initial_kwargs = kwargs.copy()
    file_run_registry.pre_start(_input_data=input_data, _context=context, **kwargs)
    input_data = {}
    file_name = os.getcwd() + "/run_conf" + str(1234) + ".data.xml"
    assert os.path.exists(file_name)
    assert kwargs == initial_kwargs
    os.remove(file_name)
