from drunc_fsm_actions.db_run_registry import DBRunRegistry

from .conftest import MockController


def test_db_run_registry(dotdrunc_file):
    db_run_registry = DBRunRegistry(
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
    db_run_registry.pre_start(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs
    input_data = {}
    db_run_registry.post_drain_dataflow(
        _input_data=input_data, _context=context, **kwargs
    )
    assert kwargs == initial_kwargs
