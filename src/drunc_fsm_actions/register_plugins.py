import importlib
import pkgutil
import sys


def register_all_plugins():
    package = sys.modules[__name__.rsplit(".", 1)[0]]  # gets drunc_fsm_actions module
    for _, modname, ispkg in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        if not ispkg:
            if modname.startswith("drunc_fsm_actions.tests."):
                continue
            if modname == "drunc_fsm_actions.register_plugins":
                continue
            if modname == "drunc_fsm_actions.utils":
                continue

            importlib.import_module(modname)
