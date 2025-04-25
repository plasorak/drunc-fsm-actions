import os

from drunc_fsm_actions.file_logbook import FileLogbook

from .conftest import MockConfiguration, MockController


def test_file_logbook(dotdrunc_file):
    configuration = MockConfiguration(file_parameters=["file_name"])
    file_logbook = FileLogbook(
        configuration=configuration,
        _dry_run=True,
    )
    input_data = {
        "run": 1234,
        "production_vs_test": "TEST",
    }
    context = MockController()
    kwargs = {"some stuff": 123, "some other stuff": 456}
    initial_kwargs = kwargs.copy()
    file_logbook.post_start(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs
    input_data = {}
    file_logbook.post_drain_dataflow(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs
    assert os.path.exists(configuration.parameters[0].value)
