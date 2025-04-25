from drunc_fsm_actions.user_provided_run_number import UserProvidedRunNumber

from .conftest import MockController


def test_user_provided_run_number(dotdrunc_file):
    user_provided_run_number = UserProvidedRunNumber(
        configuration=None,
        _dry_run=True,
    )
    input_data = {}

    kwargs = {
        "some stuff": 123,
        "some other stuff": 456,
        "trigger_rate": 1.0,
        "run_number": 1234,
        "production_vs_test": "TEST",
        "disable_data_storage": False,
    }
    initial_kwargs = kwargs.copy()

    returned_input_data = user_provided_run_number.pre_start(
        _input_data=input_data, _context=MockController(), **kwargs
    )

    assert returned_input_data["run"] == 1234
    assert returned_input_data["production_vs_test"] == "TEST"
    assert returned_input_data["disable_data_storage"] == False
    assert abs(returned_input_data["trigger_rate"] - 1.0) < 0.000001
    assert kwargs == initial_kwargs
