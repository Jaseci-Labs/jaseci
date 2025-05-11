"""The Jac Programming Language."""

from jaclang.runtimelib.machine import (
    JacMachineImpl,
    JacMachineInterface,
    JacMachineState,
    plugin_manager,
)


plugin_manager.register(JacMachineImpl)
plugin_manager.load_setuptools_entrypoints("jac")

__all__ = ["JacMachineInterface", "JacMachineState"]
