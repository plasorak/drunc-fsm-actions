import requests
from drunc_core.fsm.action_registry import register_action
from drunc_core.fsm.core import FSMAction
from drunc_core.fsm.exceptions import CannotGetRunNumber, DotDruncJsonIncorrectFormat
from drunc_core.utils.utils import get_logger
from drunc_messages.opmon.generic_pb2 import RunInfo

from drunc_fsm_actions.utils import get_dotdrunc_json, validate_run_type


class UsvcProvidedRunNumber(FSMAction):
    def __init__(self, configuration, _dry_run=False):
        self.log = get_logger("controller.usvc_run_number")
        super().__init__(name="usvc-provided-run-number")
        dotdrunc = get_dotdrunc_json()
        self.dry_run = _dry_run
        try:
            self.API_SOCKET = dotdrunc["run_number_configuration"]["socket"]
            self.API_USER = dotdrunc["run_number_configuration"]["user"]
            self.API_PSWD = dotdrunc["run_number_configuration"]["password"]
        except KeyError as exc:
            raise DotDruncJsonIncorrectFormat(
                "Malformed ~/.drunc.json, missing a key in the 'run_number_configuration' section, or the entire 'run_number_configuration' section"
            ) from exc

        self.timeout = 0.5

    def pre_start(
        self,
        _input_data: dict,
        _context,
        run_type: str = "TEST",
        disable_data_storage: bool = False,
        trigger_rate: float = 0.0,
        **kwargs,
    ):
        run_type = validate_run_type(run_type.upper())
        _input_data["production_vs_test"] = run_type
        _input_data["run"] = self._getnew_run_number()
        _input_data["disable_data_storage"] = disable_data_storage
        _input_data["trigger_rate"] = trigger_rate

        _session = _context.session
        _name = _context.name
        if _context.opmon_publisher:
            _context.opmon_publisher.publish(
                session=_session,
                application=_name,
                message=RunInfo(
                    run_type=run_type,
                    trigger_rate=trigger_rate,
                    run_number=_input_data["run"],
                    disable_data_storage=disable_data_storage,
                ),
            )

        return _input_data

    def _getnew_run_number(self):
        if self.dry_run:
            return 1
        try:
            req = requests.get(
                self.API_SOCKET + "/runnumber/getnew",
                auth=(self.API_USER, self.API_PSWD),
                timeout=self.timeout,
            )
            req.raise_for_status()
        except requests.HTTPError as exc:
            error = f"of HTTP Error (maybe failed auth, maybe ill-formed post message, ...) using {__name__}"
            self.log.error(error)
            raise CannotGetRunNumber(error) from exc
        except requests.ConnectionError as exc:
            error = (
                f"connection to {self.API_SOCKET} wasn't successful using {__name__}"
            )
            self.log.error(error)
            raise CannotGetRunNumber(error) from exc
        except requests.Timeout as exc:
            error = f"connection to {self.API_SOCKET} timed out using {__name__}"
            self.log.error(error)
            raise CannotGetRunNumber(error) from exc

        self.run = req.json()[0][0][0]
        return self.run


register_action("usvc-provided-run-number", UsvcProvidedRunNumber)
