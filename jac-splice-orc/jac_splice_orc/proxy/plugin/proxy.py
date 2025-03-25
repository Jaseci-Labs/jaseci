"""JAC Splice-Orchestrator Plugin."""

from types import ModuleType
from typing import Optional, Union

from jaclang.cli.cmdreg import cmd_registry
from jaclang.runtimelib.importer import ImportPathSpec, JacImporter, PythonImporter
from jaclang.runtimelib.machine import JacMachine, JacProgram

from pluggy import HookimplMarker

hookimpl = HookimplMarker("jac")


class ProxyPlugin:
    """Jac module proxy plugin."""

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Create Jac CLI commands."""

        @cmd_registry.register
        def verify() -> bool:
            """Verify Installation."""
            return True

    @staticmethod
    @hookimpl
    def jac_import(
        target: str,
        base_path: str,
        absorb: bool,
        cachable: bool,
        mdl_alias: Optional[str],
        override_name: Optional[str],
        lng: Optional[str],
        items: Optional[dict[str, Union[str, Optional[str]]]],
        reload_module: Optional[bool],
    ) -> tuple[ModuleType, ...]:
        """Core Import Process with Kubernetes Pod Integration."""
        spec = ImportPathSpec(
            target,
            base_path,
            absorb,
            cachable,
            mdl_alias,
            override_name,
            lng,
            items,
        )

        jac_machine = JacMachine.get(base_path)
        if not jac_machine.jac_program:
            jac_machine.attach_program(
                JacProgram(mod_bundle=None, bytecode=None, sem_ir=None)
            )

        if lng == "py":
            import_result = PythonImporter(JacMachine.get()).run_import(spec)
        else:
            import_result = JacImporter(JacMachine.get()).run_import(
                spec, reload_module
            )

        return (
            (import_result.ret_mod,)
            if absorb or not items
            else tuple(import_result.ret_items)
        )
