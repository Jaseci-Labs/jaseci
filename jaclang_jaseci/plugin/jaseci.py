"""Jac Language Features."""

from collections import OrderedDict
from dataclasses import Field, _MISSING_TYPE, is_dataclass
from functools import wraps
from os import getenv
from pydoc import locate
from re import compile
from typing import Any, Callable, Optional, Type, TypeVar, Union, cast

from fastapi import APIRouter, Depends, File, Request, Response, UploadFile
from fastapi.responses import ORJSONResponse

from jaclang.compiler.constant import EdgeDir
from jaclang.plugin.default import hookimpl
from jaclang.plugin.feature import JacFeature as Jac

from orjson import loads

from pydantic import BaseModel, Field as pyField, ValidationError, create_model

from starlette.datastructures import UploadFile as BaseUploadFile

from ..core.architype import (
    Anchor,
    Architype,
    DSFunc,
    EdgeArchitype,
    GenericEdge,
    NodeArchitype,
    Root,
    WalkerAnchor,
    WalkerArchitype,
)
from ..core.context import JaseciContext
from ..core.security import authenticator
from ..core.utils import make_optional


T = TypeVar("T")
DISABLE_AUTO_ENDPOINT = getenv("DISABLE_AUTO_ENDPOINT") == "true"
PATH_VARIABLE_REGEX = compile(r"{([^\}]+)}")
FILE = {
    "File": UploadFile,
    "Files": list[UploadFile],
    "OptFile": Optional[UploadFile],
    "OptFiles": Optional[list[UploadFile]],
}

walker_router = APIRouter(prefix="/walker", tags=["walker"])


def get_specs(cls: type) -> Optional[Type["DefaultSpecs"]]:
    """Get Specs and inherit from DefaultSpecs."""
    specs = getattr(cls, "__specs__", None)
    if specs is None:
        if DISABLE_AUTO_ENDPOINT:
            return None
        specs = DefaultSpecs

    if not issubclass(specs, DefaultSpecs):
        specs = type(specs.__name__, (specs, DefaultSpecs), {})

    return specs


def gen_model_field(cls: type, field: Field, is_file: bool = False) -> tuple[type, Any]:
    """Generate Specs for Model Field."""
    if not isinstance(field.default, _MISSING_TYPE):
        consts = (make_optional(cls), pyField(default=field.default))
    elif callable(field.default_factory):
        consts = (make_optional(cls), pyField(default_factory=field.default_factory))
    else:
        consts = (cls, File(...) if is_file else ...)

    return consts


def populate_apis(cls: type) -> None:
    """Generate FastAPI endpoint based on WalkerArchitype class."""
    if (specs := get_specs(cls)) and not specs.private:
        path: str = specs.path or ""
        methods: list = specs.methods or []
        as_query: Union[str, list] = specs.as_query or []
        auth: bool = specs.auth or False

        query: dict[str, Any] = {}
        body: dict[str, Any] = {}
        files: dict[str, Any] = {}

        if path:
            if not path.startswith("/"):
                path = f"/{path}"
            if isinstance(as_query, list):
                as_query += PATH_VARIABLE_REGEX.findall(path)

        if is_dataclass(cls):
            fields: dict[str, Field] = cls.__dataclass_fields__
            for key, val in fields.items():
                if file_type := FILE.get(cast(str, val.type)):  # type: ignore[arg-type]
                    files[key] = gen_model_field(file_type, val, True)  # type: ignore[arg-type]
                else:
                    consts = gen_model_field(locate(val.type), val)  # type: ignore[arg-type]

                    if as_query == "*" or key in as_query:
                        query[key] = consts
                    else:
                        body[key] = consts

        payload: dict[str, Any] = {
            "query": (
                create_model(f"{cls.__name__.lower()}_query_model", **query),
                Depends(),
            ),
            "files": (
                create_model(f"{cls.__name__.lower()}_files_model", **files),
                Depends(),
            ),
        }

        body_model = None
        if body:
            body_model = create_model(f"{cls.__name__.lower()}_body_model", **body)

            if files:
                payload["body"] = (UploadFile, File(...))
            else:
                payload["body"] = (body_model, ...)

        payload_model = create_model(f"{cls.__name__.lower()}_request_model", **payload)

        async def api_entry(
            request: Request,
            node: Optional[str],
            payload: payload_model = Depends(),  # type: ignore # noqa: B008
        ) -> ORJSONResponse:
            pl = cast(BaseModel, payload).model_dump()
            body = pl.get("body", {})

            if isinstance(body, BaseUploadFile) and body_model:
                body = loads(await body.read())
                try:
                    body = body_model(**body).model_dump()
                except ValidationError as e:
                    return ORJSONResponse({"detail": e.errors()})

            jctx = JaseciContext.get({"request": request, "entry": node})

            wlk: WalkerAnchor = cls(**body, **pl["query"], **pl["files"]).__jac__
            await wlk.spawn_call(jctx.entry)

            jctx.close()
            return ORJSONResponse(jctx.response(wlk.returns))

        async def api_root(
            request: Request,
            payload: payload_model = Depends(),  # type: ignore # noqa: B008
        ) -> Response:
            return await api_entry(request, None, payload)

        for method in methods:
            method = method.lower()

            walker_method = getattr(walker_router, method)

            settings: dict[str, list[Any]] = {"tags": ["walker"]}
            if auth:
                settings["dependencies"] = cast(list, authenticator)

            walker_method(url := f"/{cls.__name__}{path}", summary=url, **settings)(
                api_root
            )
            walker_method(
                url := f"/{cls.__name__}/{{node}}{path}", summary=url, **settings
            )(api_entry)


def specs(
    cls: Optional[Type[T]] = None,
    *,
    path: str = "",
    methods: list[str] = ["post"],  # noqa: B006
    as_query: Union[str, list] = [],  # noqa: B006
    auth: bool = True,
    private: bool = False,
) -> Callable:
    """Walker Decorator."""

    def wrapper(cls: Type[T]) -> Type[T]:
        if get_specs(cls) is None:
            p = path
            m = methods
            aq = as_query
            a = auth
            pv = private

            class __specs__(DefaultSpecs):  # noqa: N801
                path: str = p
                methods: list[str] = m
                as_query: Union[str, list] = aq
                auth: bool = a
                private: bool = pv

            cls.__specs__ = __specs__  # type: ignore[attr-defined]

            populate_apis(cls)
        return cls

    if cls:
        return wrapper(cls)

    return wrapper


class DefaultSpecs:
    """Default API specs."""

    path: str = ""
    methods: list[str] = ["post"]
    as_query: Union[str, list[str]] = []
    auth: bool = True
    private: bool = False


class JacPlugin:
    """Jaseci Implementations."""

    @staticmethod
    @hookimpl
    def context(options: Optional[dict[str, Any]]) -> JaseciContext:
        """Get the execution context."""
        return JaseciContext.get(options)

    @staticmethod
    @hookimpl
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a new architype."""
        for i in on_entry + on_exit:
            i.resolve(cls)
        if not hasattr(cls, "_jac_entry_funcs_") or not hasattr(
            cls, "_jac_exit_funcs_"
        ):
            # Saving the module path and reassign it after creating cls
            # So the jac modules are part of the correct module
            cur_module = cls.__module__
            cls = type(cls.__name__, (cls, arch_base), {})
            cls.__module__ = cur_module
            cls._jac_entry_funcs_ = on_entry  # type: ignore
            cls._jac_exit_funcs_ = on_exit  # type: ignore
        else:
            new_entry_funcs = OrderedDict(zip([i.name for i in on_entry], on_entry))
            entry_funcs = OrderedDict(
                zip([i.name for i in cls._jac_entry_funcs_], cls._jac_entry_funcs_)
            )
            entry_funcs.update(new_entry_funcs)
            cls._jac_entry_funcs_ = list(entry_funcs.values())

            new_exit_funcs = OrderedDict(zip([i.name for i in on_exit], on_exit))
            exit_funcs = OrderedDict(
                zip([i.name for i in cls._jac_exit_funcs_], cls._jac_exit_funcs_)
            )
            exit_funcs.update(new_exit_funcs)
            cls._jac_exit_funcs_ = list(exit_funcs.values())

        inner_init = cls.__init__  # type: ignore

        @wraps(inner_init)
        def new_init(
            self: Architype,
            *args: object,
            __jac__: Optional[Anchor] = None,
            **kwargs: object,
        ) -> None:
            arch_base.__init__(self, __jac__)
            inner_init(self, *args, **kwargs)

        cls.__init__ = new_init  # type: ignore
        return cls

    @staticmethod
    @hookimpl
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacPlugin.make_architype(
                cls=cls, arch_base=Architype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacPlugin.make_architype(
                cls=cls, arch_base=NodeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacPlugin.make_architype(
                cls=cls, arch_base=EdgeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacPlugin.make_architype(
                cls=cls, arch_base=WalkerArchitype, on_entry=on_entry, on_exit=on_exit
            )
            populate_apis(cls)
            return cls

        return decorator

    @staticmethod
    @hookimpl
    async def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Jac's spawn operator feature."""
        if isinstance(op1, WalkerArchitype):
            return await op1.__jac__.spawn_call(op2.__jac__)
        elif isinstance(op2, WalkerArchitype):
            return await op2.__jac__.spawn_call(op1.__jac__)
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""
        JaseciContext.get().reports.append(expr)

    @staticmethod
    @hookimpl
    def ignore(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
    ) -> bool:
        """Jac's ignore stmt feature."""
        if isinstance(walker, WalkerArchitype):
            return walker.__jac__.ignore_node(
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            )
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    def visit_node(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
    ) -> bool:
        """Jac's visit stmt feature."""
        if isinstance(walker, WalkerArchitype):
            return walker.__jac__.visit_node(
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            )
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    def edge_ref(
        node_obj: NodeArchitype | list[NodeArchitype],
        target_obj: Optional[NodeArchitype | list[NodeArchitype]],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's apply_dir stmt feature."""
        if isinstance(node_obj, NodeArchitype):
            node_obj = [node_obj]
        targ_obj_set: Optional[list[NodeArchitype]] = (
            [target_obj]
            if isinstance(target_obj, NodeArchitype)
            else target_obj if target_obj else None
        )
        if edges_only:
            connected_edges: list[EdgeArchitype] = []
            for node in node_obj:
                connected_edges += node.__jac__.get_edges(
                    dir, filter_func, target_obj=targ_obj_set
                )
            return list(set(connected_edges))
        else:
            connected_nodes: list[NodeArchitype] = []
            for node in node_obj:
                connected_nodes.extend(
                    node.__jac__.edges_to_nodes(
                        dir, filter_func, target_obj=targ_obj_set
                    )
                )
            return list(set(connected_nodes))

    @staticmethod
    @hookimpl
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: Callable[[], EdgeArchitype],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        left = [left] if isinstance(left, NodeArchitype) else left
        right = [right] if isinstance(right, NodeArchitype) else right
        edges = []
        for i in left:
            for j in right:
                if (source := i.__jac__).has_connect_access(target := j.__jac__):
                    conn_edge = edge_spec()
                    edges.append(conn_edge)
                    source.connect_node(target, conn_edge.__jac__)
        return right if not edges_only else edges

    @staticmethod
    @hookimpl
    def disconnect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    ) -> bool:  # noqa: ANN401
        """Jac's disconnect operator feature."""
        disconnect_occurred = False
        left = [left] if isinstance(left, NodeArchitype) else left
        right = [right] if isinstance(right, NodeArchitype) else right
        for i in left:
            node = i.__jac__
            for anchor in set(node.edges):
                if (
                    (architype := anchor.sync(node))
                    and (source := anchor.source)
                    and (target := anchor.target)
                    and (not filter_func or filter_func([architype]))
                ):
                    src_arch = source.sync()
                    trg_arch = target.sync()

                    if (
                        dir in [EdgeDir.OUT, EdgeDir.ANY]
                        and i == source
                        and trg_arch in right
                        and source.has_write_access(target)
                    ):
                        anchor.detach()
                        disconnect_occurred = True
                    if (
                        dir in [EdgeDir.IN, EdgeDir.ANY]
                        and i == target
                        and src_arch in right
                        and target.has_write_access(source)
                    ):
                        anchor.detach()
                        disconnect_occurred = True

        return disconnect_occurred

    @staticmethod
    @hookimpl
    def get_root() -> Root:
        """Jac's assign comprehension feature."""
        if architype := JaseciContext.get().root.sync():
            return cast(Root, architype)
        raise Exception("No Available Root!")

    @staticmethod
    @hookimpl
    def get_root_type() -> Type[Root]:
        """Jac's root getter."""
        return Root

    @staticmethod
    @hookimpl
    def build_edge(
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype] | EdgeArchitype],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[], EdgeArchitype]:
        """Jac's root getter."""
        conn_type = conn_type if conn_type else GenericEdge

        def builder() -> EdgeArchitype:
            edge = conn_type() if isinstance(conn_type, type) else conn_type
            edge.__jac__.is_undirected = is_undirected
            if conn_assign:
                for fld, val in zip(conn_assign[0], conn_assign[1]):
                    if hasattr(edge, fld):
                        setattr(edge, fld, val)
                    else:
                        raise ValueError(f"Invalid attribute: {fld}")
            return edge

        return builder


##########################################################
#               NEED TO TRANSFER TO PLUGIN               #
##########################################################

Jac.RootType = Root  # type: ignore[assignment]
Jac.Obj = Architype  # type: ignore[assignment]
Jac.Node = NodeArchitype  # type: ignore[assignment]
Jac.Edge = EdgeArchitype  # type: ignore[assignment]
Jac.Walker = WalkerArchitype  # type: ignore[assignment]
