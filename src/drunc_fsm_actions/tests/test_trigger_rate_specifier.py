from drunc_fsm_actions.trigger_rate_specifier import TriggerRateSpecifier


def test_trigger_rate_specifier(dotdrunc_file):
    trigger_rate_specifier = TriggerRateSpecifier(
        configuration=None,
        _dry_run=True,
    )
    input_data = {
        "run": 1234,
        "production_vs_test": "TEST",
    }

    kwargs = {"some stuff": 123, "some other stuff": 456, "trigger_rate": 1.0}

    returned_input_data = trigger_rate_specifier.pre_change_rate(
        _input_data=input_data, _context=None, **kwargs
    )

    assert abs(returned_input_data["trigger_rate"] - 1.0) < 0.000001
    assert kwargs["some stuff"] == 123
    assert kwargs["some other stuff"] == 456
    assert abs(kwargs["trigger_rate"] - 1.0) < 0.000001
