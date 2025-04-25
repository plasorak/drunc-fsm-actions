from drunc_core.fsm.action_registry import register_action
from drunc_core.fsm.core import FSMAction


class TriggerRateSpecifier(FSMAction):
    def __init__(self, configuration, _dry_run=False):
        super().__init__(name="trigger-rate-specifier")

    def pre_change_rate(
        self, _input_data: dict, _context, trigger_rate: float, **kwargs
    ):
        _input_data["trigger_rate"] = trigger_rate
        return _input_data


register_action("trigger-rate-specifier", TriggerRateSpecifier)
