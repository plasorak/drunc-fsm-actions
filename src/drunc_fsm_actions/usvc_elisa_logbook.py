import requests
from drunc_core.fsm.action_registry import register_action
from drunc_core.fsm.core import FSMAction
from drunc_core.fsm.exceptions import (
    CannotSendElisaMessage,
    DotDruncJsonIncorrectFormat,
)
from drunc_core.utils.utils import get_logger

from drunc_fsm_actions.utils import get_dotdrunc_json


class ElisaLogbook(FSMAction):
    def __init__(self, configuration, _dry_run=False) -> None:
        super().__init__(name="elisa-logbook")
        self.log = get_logger("controller.elisa-logbook")
        self.dry_run = _dry_run

        dotdrunc = get_dotdrunc_json()

        if (
            dotdrunc["elisa_configuration"].get("socket")
            or dotdrunc["elisa_configuration"].get("user")
            or dotdrunc["elisa_configuration"].get("password")
        ):
            try:
                ec = dotdrunc["elisa_configuration"]
                self.API_SOCKET = ec["socket"]
                self.API_USER = ec["user"]
                self.API_PASS = ec["password"]
            except KeyError as exc:
                msg = (
                    "Malformed ~/.drunc.json, missing a key in the"
                    "'elisa_configuration' section, or the entire"
                    "'elisa_configuration' section"
                )
                raise DotDruncJsonIncorrectFormat(
                    msg,
                ) from exc

            if len(configuration.parameters) > 0:
                self.log.error(
                    f"You need to update your ~/.drunc.json: you have specified an"
                    f" ELisA logbook ({configuration.parameters[0].value}) in your"
                    f" configuration, but your current ~/.drunc.json doesn't support"
                    f" this (if you run with this, you will get ELisA logging on"
                    f" whichever you have specified in your ~/.drunc.json). Contact"
                    f" Pierre Lasorak for help.",
                )
            else:
                self.log.warning(
                    f"Using the following ELisA endpoint: {self.API_SOCKET}."
                    " (note, you can update your ~/.drunc.json and configuration"
                    " to support logging on different ELisA logbooks). Contact"
                    " Pierre Lasorak for help.",
                )
        else:
            elisa_hardware = next(iter(dotdrunc["elisa_configuration"].keys()))
            if len(configuration.parameters) > 0:
                elisa_hardware_tmp = configuration.parameters[0].value
                if elisa_hardware_tmp not in dotdrunc["elisa_configuration"]:
                    self._log.error(
                        f"The ELisA logbook you specified in your configuration"
                        f" '{elisa_hardware_tmp}' was not found in '~/.drunc.json'."
                        f" I will use the first one in your ~/.drunc.json."
                        f" You will log on the ELisA logbook '{elisa_hardware}'."
                        " Contact Pierre Lasorak for help.",
                    )
                else:
                    elisa_hardware = elisa_hardware_tmp
            else:
                self._log.error(
                    "ELisA logbook not specified in the configuration,"
                    " using the first one in from your '~/.drunc.json'."
                    " You will log on the ELisA logbook '{elisa_hardware}'."
                    " Contact Pierre Lasorak for help.",
                )

            try:
                self.API_SOCKET = dotdrunc["elisa_configuration"][elisa_hardware][
                    "socket"
                ]
                self.API_USER = dotdrunc["elisa_configuration"][elisa_hardware]["user"]
                self.API_PASS = dotdrunc["elisa_configuration"][elisa_hardware][
                    "password"
                ]
            except KeyError as exc:
                msg = (
                    f"Malformed ~/.drunc.json, missing a key in the"
                    f"'elisa_configuration.{elisa_hardware}' section, or the entire"
                    f"'elisa_configuration.{elisa_hardware}' section"
                )
                raise DotDruncJsonIncorrectFormat(
                    msg,
                ) from exc

            self.log.info(f"Using the following ELisA logbook '{elisa_hardware}'.")
        self.timeout = 5

    def post_start(self, _input_data: dict, _context, elisa_post: str = "", **kwargs):
        text = ""
        self.thread_id = None
        # Clear this value here, so that if it fails stop can't reply to an old message

        self.run_num = _input_data["run"]
        if elisa_post != "":
            self.log.info(
                f"""Adding the message:
                --------
                {elisa_post}
                --------
                to the logbook""",
            )
            text += f"\n<p>{elisa_post}</p>"

        self.run_type = _input_data.get(
            "production_vs_test",
            "TEST",
        )

        text += f"Configuration: {_context.configuration.initial_data}"

        if elisa_post != "" and self.run_type.lower() != "prod":
            self.log.warning(
                "Your message will NOT be stored, as this is not a PROD run",
            )

        text += "\n<p>log automatically generated by DRunC.</p>"
        self.det_id = _context.configuration.db.get_dal(
            class_name="Session",
            uid=_context.configuration.oks_key.session,
        ).detector_configuration.id
        title = f"Run {self.run_num} ({self.run_type}) started on {self.det_id}"
        data = {
            "author": _context.actor.get_user_name(),
            "title": title,
            "body": text,
            "command": "start",
            "systems": ["daq"],
        }
        url = f"{self.API_SOCKET}/v1/elisaLogbook/new_message/"
        if not self.dry_run:
            try:
                r = requests.post(url, auth=(self.API_USER, self.API_PASS), json=data)
                r.raise_for_status()
                response = r.json()
                self.thread_id = response["thread_id"]
                self.log.info(f"ELisA logbook: Sent message (ID{self.thread_id})")
            except requests.HTTPError:
                error = (
                    "of HTTP Error (maybe failed auth, maybe ill-formed"
                    "post message, ...) using {__name__}"
                )
                self.log.warning(CannotSendElisaMessage(error).message)
            except requests.ConnectionError:
                error = (
                    f"connection to {self.API_SOCKET} wasn't successful using"
                    f" {__name__}"
                )
                self.log.warning(CannotSendElisaMessage(error).message)
            except requests.Timeout:
                error = f"connection to {self.API_SOCKET} timed out using {__name__}"
            self.log.warning(CannotSendElisaMessage(error).message)

        return _input_data

    def post_drain_dataflow(
        self,
        _input_data,
        _context,
        elisa_post: str = "",
        **kwargs,
    ):
        text = ""
        if elisa_post != "":
            self.log.info(
                f"""Adding the message:
                --------
                {elisa_post}
                --------
                to the logbook""",
            )
            text += f"\n<p>{elisa_post}</p>"

        text += f"Run {self.run_num} ({self.run_type}) stopped on {self.det_id}"
        text += "\n<p>log automatically generated by DRunC.</p>"
        title = "User comment"
        data = {
            "author": _context.actor.get_user_name(),
            "title": title,
            "body": text,
            "command": "stop",
            "systems": ["daq"],
            "id": self.thread_id,
        }
        url = f"{self.API_SOCKET}/v1/elisaLogbook/reply_to_message/"
        if not self.dry_run:
            try:
                r = requests.put(url, auth=(self.API_USER, self.API_PASS), json=data)
                r.raise_for_status()
                response = r.json()
                self.log.info(
                    f"ELisA logbook: Sent message (ID{response['thread_id']})",
                )
            except requests.HTTPError:
                error = (
                    "of HTTP Error (maybe failed auth, maybe ill-formed"
                    "post message, ...) using {__name__}"
                )
                self.log.warning(CannotSendElisaMessage(error).message)
            except requests.ConnectionError:
                error = (
                    f"connection to {self.API_SOCKET} wasn't successful using"
                    f" {__name__}"
                )
                self.log.warning(CannotSendElisaMessage(error).message)
            except requests.Timeout:
                error = f"connection to {self.API_SOCKET} timed out using {__name__}"
                self.log.warning(CannotSendElisaMessage(error).message)

        return _input_data


register_action("elisa-logbook", ElisaLogbook)
