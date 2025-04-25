from drunc_fsm_actions.usvc_elisa_logbook import ElisaLogbook

from .conftest import MockConfiguration, MockController


def test_usvc_elisa_logbook(dotdrunc_file):
    elisa_logbook = ElisaLogbook(
        configuration=MockConfiguration(parameters={"elisa_logbook": "some-detector"}),
        _dry_run=True,
    )
    input_data = {
        "run": 1234,
        "production_vs_test": "TEST",
        "disable_data_storage": False,
        "trigger_rate": 1.0,
    }

    kwargs = {"some stuff": 123, "some other stuff": 456}

    elisa_logbook.post_start(
        _input_data=input_data, _context=MockController(), **kwargs
    )
    elisa_logbook.post_drain_dataflow(
        _input_data=input_data, _context=MockController(), **kwargs
    )
