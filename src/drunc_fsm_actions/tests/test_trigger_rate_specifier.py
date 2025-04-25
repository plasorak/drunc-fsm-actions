import pytest

from drunc_fsm_actions.trigger_rate_specifier import TriggerRateSpecifier


def test_trigger_rate_specifier(dotdrunc_file) -> None:
    trigger_rate_specifier = TriggerRateSpecifier(
        configuration=None,
        _dry_run=True,
    )
    input_data = {
        "run": 1234,
        "production_vs_test": "TEST",
    }
    some_stuff = 123
    some_other_stuff = 456
    trigger_rate = 1.0
    kwargs = {
        "some stuff": some_stuff,
        "some other stuff": some_other_stuff,
        "trigger_rate": trigger_rate,
    }

    returned_input_data = trigger_rate_specifier.pre_change_rate(
        _input_data=input_data,
        _context=None,
        **kwargs,
    )

    assert pytest.approx(returned_input_data["trigger_rate"], trigger_rate)
    assert kwargs["some stuff"] == some_stuff
    assert kwargs["some other stuff"] == some_other_stuff
    assert pytest.approx(kwargs["trigger_rate"], trigger_rate)
