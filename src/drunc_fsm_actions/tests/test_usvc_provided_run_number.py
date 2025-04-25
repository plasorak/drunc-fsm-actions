from drunc_fsm_actions.usvc_provided_run_number import UsvcProvidedRunNumber

from .conftest import MockController


def test_usvc_provided_run_number(dotdrunc_file):
    usvc_provided_run_number = UsvcProvidedRunNumber(
        configuration=None,
        _dry_run=True,
    )
    input_data = {}

    kwargs = {
        "some stuff": 123,
        "some other stuff": 456,
        "trigger_rate": 1.0,
        "production_vs_test": "TEST",
        "disable_data_storage": False,
    }
    initial_kwargs = kwargs.copy()

    returned_input_data = usvc_provided_run_number.pre_start(
        _input_data=input_data, _context=MockController(), **kwargs
    )

    assert returned_input_data["run"] == 1
    assert returned_input_data["production_vs_test"] == "TEST"
    assert returned_input_data["disable_data_storage"] == False
    assert abs(returned_input_data["trigger_rate"] - 1.0) < 0.000001
    assert kwargs == initial_kwargs
