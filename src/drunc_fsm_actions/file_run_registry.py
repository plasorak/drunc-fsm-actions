import os

from daqconf.consolidate import consolidate_db
from drunc_core.fsm.action_registry import register_action
from drunc_core.fsm.core import FSMAction


class FileRunRegistry(FSMAction):
    def __init__(self, configuration, _dry_run=False) -> None:
        super().__init__(name="file-run-registry")
        self.configuration = configuration
        self.dry_run = _dry_run

    def pre_start(self, _input_data, _context, **kwargs):
        run_number = _input_data["run"]
        dest = os.getcwd() + "/run_conf" + str(run_number) + ".data.xml"
        consolidate_db(_context.configuration.initial_data.split(":")[1], f"{dest}")

        return _input_data


register_action("file-run-registry", FileRunRegistry)
