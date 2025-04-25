import os

import pytest

from drunc_fsm_actions.thread_pinning import ThreadPinning, ThreadPinningFailed

from .conftest import MockConfiguration, MockController


def test_thread_pinning(dotdrunc_file):
    parameters = {
        "post_conf": "pinning_file.junk",
        "post_start": "pinning_file.junk",
        "pre_conf": "pinning_file.junk",
    }
    configuration = MockConfiguration(parameters=parameters)
    thread_pinning = ThreadPinning(
        configuration=configuration,
        _dry_run=True,
    )
    input_data = {}
    context = MockController()
    kwargs = {"some stuff": 123, "some other stuff": 456}
    initial_kwargs = kwargs.copy()

    with pytest.raises(ThreadPinningFailed):
        thread_pinning.post_conf(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs

    with pytest.raises(ThreadPinningFailed):
        thread_pinning.post_start(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs

    with pytest.raises(ThreadPinningFailed):
        thread_pinning.pre_conf(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs

    cpu_pinning_file = (
        os.getenv("DATAHANDLINGLIBS_SHARE") + "/config/cpupins/cpupin-example.json"
    )
    parameters = {
        "post_conf": cpu_pinning_file,
        "post_start": cpu_pinning_file,
        "pre_conf": cpu_pinning_file,
    }
    configuration = MockConfiguration(parameters=parameters)
    thread_pinning = ThreadPinning(
        configuration=configuration,
        _dry_run=True,
    )
    input_data = {}
    context = MockController()
    kwargs = {"some stuff": 123, "some other stuff": 456}
    initial_kwargs = kwargs.copy()

    thread_pinning.post_conf(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs

    thread_pinning.post_start(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs

    thread_pinning.pre_conf(_input_data=input_data, _context=context, **kwargs)
    assert kwargs == initial_kwargs
