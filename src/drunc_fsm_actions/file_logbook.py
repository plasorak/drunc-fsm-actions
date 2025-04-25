from drunc_core.fsm.action_registry import register_action
from drunc_core.fsm.core import FSMAction
from drunc_core.utils.utils import now_str


class FileLogbook(FSMAction):
    def __init__(self, configuration, _dry_run=False) -> None:
        super().__init__(name="file-logbook")
        self.dry_run = _dry_run
        self.conf_dict = {p.name: p.value for p in configuration.parameters}
        self.file = self.conf_dict["file_name"]

    def post_start(self, _input_data, _context, file_logbook_post: str = "", **kwargs):
        with open(self.file, "a") as f:
            f.write(
                f"Run {_input_data['run']} started by {_context.actor.get_user_name()}"
                f" at {now_str()}\n",
            )
            if file_logbook_post != "":
                f.write(file_logbook_post)
                f.write("\n")

        return _input_data

    def post_drain_dataflow(
        self,
        _input_data,
        _context,
        file_logbook_post: str = "",
        **kwargs,
    ):
        with open(self.file, "a") as f:
            f.write(
                f"Current run stopped by {_context.actor.get_user_name()}"
                f"at {now_str()}\n",
            )
            if file_logbook_post != "":
                f.write(file_logbook_post)
                f.write("\n")

        return _input_data


register_action("file-logbook", FileLogbook)
