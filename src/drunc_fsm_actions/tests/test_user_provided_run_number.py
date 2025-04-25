import pytest

from drunc_fsm_actions.user_provided_run_number import UserProvidedRunNumber

from .conftest import MockController


def test_user_provided_run_number(dotdrunc_file) -> None:
    user_provided_run_number = UserProvidedRunNumber(
        configuration=None,
        _dry_run=True,
    )
    input_data = {}
    some_stuff = 123
    some_other_stuff = 456
    trigger_rate = 1.0
    run_number = 1234
    production_vs_test = "TEST"
    disable_data_storage = False

    kwargs = {
        "some stuff": some_stuff,
        "some other stuff": some_other_stuff,
        "trigger_rate": trigger_rate,
        "run_number": run_number,
        "production_vs_test": production_vs_test,
        "disable_data_storage": disable_data_storage,
    }
    initial_kwargs = kwargs.copy()

    returned_input_data = user_provided_run_number.pre_start(
        _input_data=input_data,
        _context=MockController(),
        **kwargs,
    )

    assert returned_input_data["run"] == run_number
    assert returned_input_data["production_vs_test"] == production_vs_test
    assert returned_input_data["disable_data_storage"] == disable_data_storage
    assert pytest.approx(returned_input_data["trigger_rate"], trigger_rate)
    assert kwargs == initial_kwargs
