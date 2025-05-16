"""The Jac Programming Language."""

from jaclang.runtimelib.machine import (
    JacMachine,
    JacMachineImpl,
    JacMachineInterface,
    plugin_manager,
)


plugin_manager.register(JacMachineImpl)
plugin_manager.load_setuptools_entrypoints("jac")

__all__ = ["JacMachineInterface", "JacMachine"]
