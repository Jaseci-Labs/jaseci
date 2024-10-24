"""JAC Splice-Orchestrator Plugin."""

import types
from typing import Optional, Union

from jaclang.runtimelib.importer import ImportPathSpec, JacImporter, PythonImporter
from jaclang.runtimelib.machine import JacMachine, JacProgram
from jaclang.settings import settings

from managers.proxy_manager import ModuleProxy

import pluggy


hookimpl = pluggy.HookimplMarker("jac")


class SpliceOrcPlugin:
    """JAC Splice-Orchestrator Plugin."""

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
    ) -> tuple[types.ModuleType, ...]:
        """Core Import Process with Kubernetes Pod Integration."""
        if (
            target in settings.module_config
            and settings.module_config[target]["load_type"] == "remote"
        ):
            proxy = ModuleProxy(settings.pod_manager_url)
            print(f"Loading Kubernetes Pod Integration")
            remote_module_proxy = proxy.get_module_proxy(
                module_name=target, module_config=settings.module_config[target]
            )

            return (remote_module_proxy,)

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
            jac_machine.attach_program(JacProgram(mod_bundle=None, bytecode=None))

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
