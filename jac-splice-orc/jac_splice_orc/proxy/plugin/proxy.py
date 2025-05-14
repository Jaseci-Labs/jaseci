"""JAC Splice-Orchestrator Plugin."""

from pickle import dumps, loads
from types import ModuleType
from typing import Any

from grpc import RpcError, insecure_channel

from jac_splice_orc.proxy.grpc_local import module_service_pb2
from jac_splice_orc.proxy.grpc_local.module_service_pb2_grpc import ModuleServiceStub

from jaclang.cli.cmdreg import cmd_registry
from jaclang.runtimelib.machine import JacMachine, JacMachineImpl, hookimpl


class ProxyObject:
    """Proxy Object Handler."""

    def __init__(self, stub: ModuleServiceStub, id: str, module: str) -> None:
        """Override init."""
        self.stub = stub
        self.id = id
        self.module = module

    def __getattr__(self, attr: str) -> Any:
        """Override getattr."""
        try:
            request = module_service_pb2.AttributeRequest(  # type: ignore[attr-defined]
                id=self.id, attribute=attr
            )
            response = self.stub.get_attribute(request)
            if response.type < 0:
                value = loads(response.bytes_value)
            elif response.type > 1:
                value = CallableProxyObject(self.stub, response.string_value, "")
            else:
                value = ProxyObject(self.stub, response.string_value, "")

            if response.type < 1:
                setattr(self, attr, value)
            return value

        except RpcError:
            raise

    def __repr__(self) -> str:
        """Override repr."""
        request = module_service_pb2.MethodRequest(  # type: ignore[attr-defined]
            id=self.id, method="__repr__"
        )
        response = self.stub.execute(request)
        return loads(response.bytes_value)


class CallableProxyObject(ProxyObject):
    """Callable Proxy Object Handler."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Trigger proxy call."""
        try:
            arguments = [
                (
                    module_service_pb2.MethodArgument(  # type: ignore[attr-defined]
                        proxy=True, string_value=arg.id
                    )
                    if isinstance(arg, ProxyObject)
                    else module_service_pb2.MethodArgument(  # type: ignore[attr-defined]
                        proxy=False, bytes_value=dumps(arg)
                    )
                )
                for arg in args
            ]

            keywords = {
                key: (
                    module_service_pb2.MethodArgument(  # type: ignore[attr-defined]
                        proxy=True, string_value=value.id
                    )
                    if isinstance(value, ProxyObject)
                    else module_service_pb2.MethodArgument(  # type: ignore[attr-defined]
                        proxy=False, bytes_value=dumps(value)
                    )
                )
                for key, value in kwargs.items()
            }

            request = module_service_pb2.MethodRequest(  # type: ignore[attr-defined]
                id=self.id, args=arguments, kwargs=keywords
            )
            response = self.stub.execute(request)

            if response.type < 0:
                return loads(response.bytes_value)
            if response.type > 0:
                return CallableProxyObject(self.stub, response.string_value, "")
            return ProxyObject(self.stub, response.string_value, "")
        except RpcError:
            raise


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
        mach: JacMachine,
        target: str,
        base_path: str,
        absorb: bool,
        mdl_alias: str | None,
        override_name: str | None,
        lng: str | None,
        items: dict[str, str | None] | None,
        reload_module: bool | None,
    ) -> tuple[ModuleType | ProxyObject, ...]:
        """Core Import Process."""
        module = target.split(".")
        if module[0] in ["numpy"]:
            stub = ModuleServiceStub(insecure_channel("localhost:50051"))
            po = ProxyObject(stub, "", "numpy")
            return (po,)

        return JacMachineImpl.jac_import(
            mach=mach,
            target=target,
            base_path=base_path,
            absorb=absorb,
            mdl_alias=mdl_alias,
            override_name=override_name,
            lng=lng,
            items=items,
            reload_module=reload_module,
        )
