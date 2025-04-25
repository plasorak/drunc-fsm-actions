import pytest

from drunc_fsm_actions.usvc_provided_run_number import UsvcProvidedRunNumber

from .conftest import MockController


def test_usvc_provided_run_number(dotdrunc_file) -> None:
    usvc_provided_run_number = UsvcProvidedRunNumber(
        configuration=None,
        _dry_run=True,
    )
    input_data = {}
    some_stuff = 123
    some_other_stuff = 456
    trigger_rate = 1.0
    production_vs_test = "TEST"
    disable_data_storage = False

    dry_run_run_number = 1

    kwargs = {
        "some stuff": some_stuff,
        "some other stuff": some_other_stuff,
        "trigger_rate": trigger_rate,
        "production_vs_test": production_vs_test,
        "disable_data_storage": disable_data_storage,
    }
    initial_kwargs = kwargs.copy()

    returned_input_data = usvc_provided_run_number.pre_start(
        _input_data=input_data,
        _context=MockController(),
        **kwargs,
    )

    assert returned_input_data["run"] == dry_run_run_number
    assert returned_input_data["production_vs_test"] == production_vs_test
    assert returned_input_data["disable_data_storage"] == disable_data_storage
    assert pytest.approx(returned_input_data["trigger_rate"], trigger_rate)
    assert kwargs == initial_kwargs
