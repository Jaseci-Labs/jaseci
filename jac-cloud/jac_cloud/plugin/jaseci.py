"""Jac Language Features."""

from collections import OrderedDict
from contextlib import suppress
from dataclasses import Field, MISSING, fields, is_dataclass
from functools import wraps
from os import getenv
from re import compile
from types import NoneType
from typing import Any, Callable, Type, TypeAlias, TypeVar, Union, cast, get_type_hints

from asyncer import syncify

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
)
from fastapi.responses import ORJSONResponse

from jaclang.compiler.constant import EdgeDir
from jaclang.plugin.default import JacFeatureImpl, hookimpl
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.architype import DSFunc

from orjson import loads

from pydantic import BaseModel, Field as pyField, ValidationError, create_model

from starlette.datastructures import UploadFile as BaseUploadFile

from ..core.architype import (
    AccessLevel,
    Anchor,
    AnchorState,
    Architype,
    BaseAnchor,
    EdgeAnchor,
    EdgeArchitype,
    GenericEdge,
    NodeAnchor,
    NodeArchitype,
    ObjectArchitype,
    Permission,
    Root,
    WalkerAnchor,
    WalkerArchitype,
)
from ..core.context import ContextResponse, ExecutionContext, JaseciContext
from ..jaseci import FastAPI
from ..jaseci.security import authenticator
from ..jaseci.utils import log_entry, log_exit


T = TypeVar("T")
DISABLE_AUTO_ENDPOINT = getenv("DISABLE_AUTO_ENDPOINT") == "true"
PATH_VARIABLE_REGEX = compile(r"{([^\}]+)}")
FILE_TYPES = {
    UploadFile,
    list[UploadFile],
    UploadFile | None,
    list[UploadFile] | None,
}

walker_router = APIRouter(prefix="/walker", tags=["walker"])


def get_specs(cls: type) -> Type["DefaultSpecs"] | None:
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
    if field.default is not MISSING:
        consts = (cls, pyField(default=field.default))
    elif callable(field.default_factory):
        consts = (cls, pyField(default_factory=field.default_factory))
    else:
        consts = (cls, File(...) if is_file else ...)

    return consts


def populate_apis(cls: Type[WalkerArchitype]) -> None:
    """Generate FastAPI endpoint based on WalkerArchitype class."""
    if (specs := get_specs(cls)) and not specs.private:
        path: str = specs.path or ""
        methods: list = specs.methods or []
        as_query: str | list[str] = specs.as_query or []
        excluded: str | list[str] = specs.excluded or []
        auth: bool = specs.auth or False

        query: dict[str, Any] = {}
        body: dict[str, Any] = {}
        files: dict[str, Any] = {}

        if path:
            if not path.startswith("/"):
                path = f"/{path}"
            if isinstance(as_query, list):
                as_query += PATH_VARIABLE_REGEX.findall(path)

        hintings = get_type_hints(cls)

        if is_dataclass(cls):
            if excluded != "*":
                if isinstance(excluded, str):
                    excluded = [excluded]

                for f in fields(cls):
                    if f.name in excluded:
                        if f.default is MISSING and not callable(f.default_factory):
                            raise AttributeError(
                                f"{cls.__name__} {f.name} should have default or default_factory."
                            )
                        continue

                    f_name = f.name
                    f_type = hintings[f_name]
                    if f_type in FILE_TYPES:
                        files[f_name] = gen_model_field(f_type, f, True)
                    else:
                        consts = gen_model_field(f_type, f)

                        if as_query == "*" or f_name in as_query:
                            query[f_name] = consts
                        else:
                            body[f_name] = consts
            elif any(
                f.default is MISSING and not callable(f.default_factory)
                for f in fields(cls)
            ):
                raise AttributeError(
                    f"{cls.__name__} fields should all have default or default_factory."
                )

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

        def api_entry(
            request: Request,
            node: str | None,
            payload: payload_model = Depends(),  # type: ignore # noqa: B008
        ) -> ORJSONResponse:
            pl = cast(BaseModel, payload).model_dump()
            body = pl.get("body", {})

            log = log_entry(
                cls.__name__,
                user.email if (user := getattr(request, "_user", None)) else None,
                pl,
                node,
            )

            if isinstance(body, BaseUploadFile) and body_model:
                body = loads(syncify(body.read)())
                try:
                    body = body_model(**body).model_dump()
                except ValidationError as e:
                    return ORJSONResponse({"detail": e.errors()})

            jctx = JaseciContext.create(request, NodeAnchor.ref(node) if node else None)

            wlk: WalkerAnchor = cls(**body, **pl["query"], **pl["files"]).__jac__
            if Jac.check_read_access(jctx.entry_node):
                Jac.spawn_call(wlk.architype, jctx.entry_node.architype)
                jctx.close()

                if jctx.custom is not MISSING:
                    return jctx.custom

                resp = jctx.response(wlk.returns)
                log_exit(resp, log)

                return ORJSONResponse(resp, jctx.status)
            else:
                error = {
                    "error": f"You don't have access on target entry{cast(Anchor, jctx.entry_node).ref_id}!"
                }
                jctx.close()

                log_exit(error, log)
                raise HTTPException(403, error)

        def api_root(
            request: Request,
            payload: payload_model = Depends(),  # type: ignore # noqa: B008
        ) -> Response:
            return api_entry(request, None, payload)

        for method in methods:
            method = method.lower()

            walker_method = getattr(walker_router, method)

            raw_types: list[Type] = [
                get_type_hints(jef.func).get("return", NoneType)
                for jef in (*cls._jac_entry_funcs_, *cls._jac_exit_funcs_)
            ]

            if raw_types:
                if len(raw_types) > 1:
                    ret_types: TypeAlias = Union[*raw_types]  # type: ignore[valid-type]
                else:
                    ret_types = raw_types[0]  # type: ignore[misc]
            else:
                ret_types = NoneType  # type: ignore[misc]

            settings: dict[str, Any] = {
                "tags": ["walker"],
                "response_model": ContextResponse[ret_types] | Any,
            }
            if auth:
                settings["dependencies"] = cast(list, authenticator)

            walker_method(url := f"/{cls.__name__}{path}", summary=url, **settings)(
                api_root
            )
            walker_method(
                url := f"/{cls.__name__}/{{node}}{path}", summary=url, **settings
            )(api_entry)


def specs(
    cls: Type[WalkerArchitype] | None = None,
    *,
    path: str = "",
    methods: list[str] = ["post"],  # noqa: B006
    as_query: str | list[str] = [],  # noqa: B006
    excluded: str | list[str] = [],  # noqa: B006
    auth: bool = True,
    private: bool = False,
) -> Callable:
    """Walker Decorator."""

    def wrapper(cls: Type[WalkerArchitype]) -> Type[WalkerArchitype]:
        if get_specs(cls) is None:
            p = path
            m = methods
            aq = as_query
            ex = excluded
            a = auth
            pv = private

            class __specs__(DefaultSpecs):  # noqa: N801
                path: str = p
                methods: list[str] = m
                as_query: str | list[str] = aq
                excluded: str | list[str] = ex
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
    as_query: str | list[str] = []
    excluded: str | list[str] = []
    auth: bool = True
    private: bool = False


class JacAccessValidationPlugin:
    """Jac Access Validation Implementations."""

    @staticmethod
    @hookimpl
    def allow_root(
        architype: Architype, root_id: BaseAnchor, level: AccessLevel | int | str
    ) -> None:
        """Allow all access from target root graph to current Architype."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.allow_root(
                architype=architype, root_id=root_id, level=level  # type: ignore[arg-type]
            )
            return

        anchor = architype.__jac__

        level = AccessLevel.cast(level)
        access = anchor.access.roots
        if (
            isinstance(anchor, BaseAnchor)
            and (ref_id := root_id.ref_id)
            and level != access.anchors.get(ref_id, AccessLevel.NO_ACCESS)
        ):
            access.anchors[ref_id] = level
            anchor._set.update({f"access.roots.anchors.{ref_id}": level.name})
            anchor._unset.pop(f"access.roots.anchors.{ref_id}", None)

    @staticmethod
    @hookimpl
    def disallow_root(
        architype: Architype, root_id: BaseAnchor, level: AccessLevel | int | str
    ) -> None:
        """Disallow all access from target root graph to current Architype."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.disallow_root(
                architype=architype, root_id=root_id, level=level  # type: ignore[arg-type]
            )
            return

        anchor = architype.__jac__

        level = AccessLevel.cast(level)
        access = anchor.access.roots
        if (
            isinstance(anchor, BaseAnchor)
            and (ref_id := root_id.ref_id)
            and access.anchors.pop(ref_id, None) is not None
        ):
            anchor._unset.update({f"access.roots.anchors.{ref_id}": True})
            anchor._set.pop(f"access.roots.anchors.{ref_id}", None)

    @staticmethod
    @hookimpl
    def unrestrict(architype: Architype, level: AccessLevel | int | str) -> None:
        """Allow everyone to access current Architype."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.unrestrict(architype=architype, level=level)
            return

        anchor = architype.__jac__

        level = AccessLevel.cast(level)
        if isinstance(anchor, BaseAnchor) and level != anchor.access.all:
            anchor.access.all = level
            anchor._set.update({"access.all": level.name})

    @staticmethod
    @hookimpl
    def restrict(architype: Architype) -> None:
        """Disallow others to access current Architype."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.restrict(architype=architype)
            return

        anchor = architype.__jac__

        if isinstance(anchor, BaseAnchor) and anchor.access.all > AccessLevel.NO_ACCESS:
            anchor.access.all = AccessLevel.NO_ACCESS
            anchor._set.update({"access.all": AccessLevel.NO_ACCESS.name})

    @staticmethod
    @hookimpl
    def check_access_level(to: Anchor) -> AccessLevel:
        """Access validation."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.check_access_level(to=to)

        if not to.persistent:
            return AccessLevel.WRITE

        from ..core.context import JaseciContext

        jctx = JaseciContext.get()

        jroot = jctx.root

        # if current root is system_root
        # if current root id is equal to target anchor's root id
        # if current root is the target anchor
        if jroot == jctx.system_root or jroot.id == to.root or jroot == to:
            return AccessLevel.WRITE

        access_level = AccessLevel.NO_ACCESS

        # if target anchor have set access.all
        if (to_access := to.access).all > AccessLevel.NO_ACCESS:
            access_level = to_access.all

        # if target anchor's root have set allowed roots
        # if current root is allowed to the whole graph of target anchor's root
        if to.root and isinstance(
            to_root := jctx.mem.find_by_id(NodeAnchor.ref(f"n::{to.root}")), Anchor
        ):
            if to_root.access.all > access_level:
                access_level = to_root.access.all

            level = to_root.access.roots.check(jroot.ref_id)
            if level > AccessLevel.NO_ACCESS and access_level == AccessLevel.NO_ACCESS:
                access_level = level

        # if target anchor have set allowed roots
        # if current root is allowed to target anchor
        level = to_access.roots.check(jroot.ref_id)
        if level > AccessLevel.NO_ACCESS and access_level == AccessLevel.NO_ACCESS:
            access_level = level

        return access_level


class JacNodePlugin:
    """Jac Node Operations."""

    @staticmethod
    @hookimpl
    def get_edges(
        node: NodeAnchor,
        dir: EdgeDir,
        filter_func: Callable[[list[EdgeArchitype]], list[EdgeArchitype]] | None,
        target_obj: list[NodeArchitype] | None,
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        if FastAPI.is_enabled():
            JaseciContext.get().mem.populate_data(node.edges)

        return JacFeatureImpl.get_edges(
            node=node, dir=dir, filter_func=filter_func, target_obj=target_obj  # type: ignore[arg-type, return-value]
        )

    @staticmethod
    @hookimpl
    def edges_to_nodes(
        node: NodeAnchor,
        dir: EdgeDir,
        filter_func: Callable[[list[EdgeArchitype]], list[EdgeArchitype]] | None,
        target_obj: list[NodeArchitype] | None,
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        if FastAPI.is_enabled():
            JaseciContext.get().mem.populate_data(node.edges)

        return JacFeatureImpl.edges_to_nodes(
            node=node, dir=dir, filter_func=filter_func, target_obj=target_obj  # type: ignore[arg-type, return-value]
        )


class JacEdgePlugin:
    """Jac Edge Operations."""

    @staticmethod
    @hookimpl
    def detach(edge: EdgeAnchor) -> None:
        """Detach edge from nodes."""
        if not FastAPI.is_enabled():
            JacFeatureImpl.detach(edge=edge)
            return

        Jac.remove_edge(node=edge.source, edge=edge)
        edge.source.disconnect_edge(edge)

        Jac.remove_edge(node=edge.target, edge=edge)
        edge.target.disconnect_edge(edge)


class JacPlugin(JacAccessValidationPlugin, JacNodePlugin, JacEdgePlugin):
    """Jaseci Implementations."""

    @staticmethod
    @hookimpl
    def get_context() -> ExecutionContext:
        """Get current execution context."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.get_context()

        return JaseciContext.get()

    @staticmethod
    @hookimpl
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a new architype."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_architype(
                cls=cls, arch_base=arch_base, on_entry=on_entry, on_exit=on_exit
            )
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
        def new_init(self: Architype, *args: object, **kwargs: object) -> None:
            arch_base.__init__(self)
            inner_init(self, *args, **kwargs)

        cls.__init__ = new_init  # type: ignore
        return cls

    @staticmethod
    @hookimpl
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_obj(on_entry=on_entry, on_exit=on_exit)

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls,
                arch_base=ObjectArchitype,
                on_entry=on_entry,
                on_exit=on_exit,
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_node(on_entry=on_entry, on_exit=on_exit)

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
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
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_edge(on_entry=on_entry, on_exit=on_exit)

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
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
        if not FastAPI.is_enabled():
            return JacFeatureImpl.make_walker(on_entry=on_entry, on_exit=on_exit)

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls,
                arch_base=WalkerArchitype,
                on_entry=on_entry,
                on_exit=on_exit,
            )
            populate_apis(cls)  # type: ignore[arg-type]
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def get_root() -> Root:
        """Jac's assign comprehension feature."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.get_root()  # type:ignore[return-value]

        return JaseciContext.get_root()

    @staticmethod
    @hookimpl
    def get_root_type() -> Type[Root]:
        """Jac's root getter."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.get_root_type()  # type:ignore[return-value]

        return Root

    @staticmethod
    @hookimpl
    def build_edge(
        is_undirected: bool,
        conn_type: Type[EdgeArchitype] | EdgeArchitype | None,
        conn_assign: tuple[tuple, tuple] | None,
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.build_edge(  # type:ignore[return-value]
                is_undirected=is_undirected,
                conn_type=conn_type,
                conn_assign=conn_assign,
            )

        conn_type = conn_type if conn_type else GenericEdge

        def builder(source: NodeAnchor, target: NodeAnchor) -> EdgeArchitype:
            edge = conn_type() if isinstance(conn_type, type) else conn_type

            eanch = edge.__jac__ = EdgeAnchor(
                architype=edge,
                name=("" if isinstance(edge, GenericEdge) else edge.__class__.__name__),
                source=source,
                target=target,
                is_undirected=is_undirected,
                access=Permission(),
                state=AnchorState(),
            )
            source.edges.append(eanch)
            target.edges.append(eanch)
            source.connect_edge(eanch)
            target.connect_edge(eanch)

            if conn_assign:
                for fld, val in zip(conn_assign[0], conn_assign[1]):
                    if hasattr(edge, fld):
                        setattr(edge, fld, val)
                    else:
                        raise ValueError(f"Invalid attribute: {fld}")
            if source.persistent or target.persistent:
                Jac.save(eanch)
                Jac.save(target)
                Jac.save(source)
            return edge

        return builder

    @staticmethod
    @hookimpl
    def get_object(id: str) -> Architype | None:
        """Get object via reference id."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.get_object(id=id)

        with suppress(ValueError):
            if isinstance(architype := BaseAnchor.ref(id).architype, Architype):
                return architype

        return None

    @staticmethod
    @hookimpl
    def object_ref(obj: Architype) -> str:
        """Get object reference id."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.object_ref(obj=obj)

        return str(obj.__jac__.ref_id)

    @staticmethod
    @hookimpl
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Invoke data spatial call."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.spawn_call(
                op1=op1, op2=op2
            )  # type:ignore[return-value]

        if isinstance(op1, WalkerArchitype):
            warch = op1
            walker = op1.__jac__
            if isinstance(op2, NodeArchitype):
                node = op2.__jac__
            elif isinstance(op2, EdgeArchitype):
                node = op2.__jac__.target
            else:
                raise TypeError("Invalid target object")
        elif isinstance(op2, WalkerArchitype):
            warch = op2
            walker = op2.__jac__
            if isinstance(op1, NodeArchitype):
                node = op1.__jac__
            elif isinstance(op1, EdgeArchitype):
                node = op1.__jac__.target
            else:
                raise TypeError("Invalid target object")
        else:
            raise TypeError("Invalid walker object")

        walker.path = []
        walker.next = [node]
        walker.returns = []

        if walker.next:
            current_node = walker.next[-1].architype
            for i in warch._jac_entry_funcs_:
                if not i.trigger:
                    if i.func:
                        walker.returns.append(i.func(warch, current_node))
                    else:
                        raise ValueError(f"No function {i.name} to call.")
        while len(walker.next):
            if current_node := walker.next.pop(0).architype:
                for i in current_node._jac_entry_funcs_:
                    if not i.trigger or isinstance(walker, i.trigger):
                        if i.func:
                            walker.returns.append(i.func(current_node, warch))
                        else:
                            raise ValueError(f"No function {i.name} to call.")
                    if walker.disengaged:
                        return warch
                for i in warch._jac_entry_funcs_:
                    if not i.trigger or isinstance(current_node, i.trigger):
                        if i.func and i.trigger:
                            walker.returns.append(i.func(warch, current_node))
                        elif not i.trigger:
                            continue
                        else:
                            raise ValueError(f"No function {i.name} to call.")
                    if walker.disengaged:
                        return warch
                for i in warch._jac_exit_funcs_:
                    if not i.trigger or isinstance(current_node, i.trigger):
                        if i.func and i.trigger:
                            walker.returns.append(i.func(warch, current_node))
                        elif not i.trigger:
                            continue
                        else:
                            raise ValueError(f"No function {i.name} to call.")
                    if walker.disengaged:
                        return warch
                for i in current_node._jac_exit_funcs_:
                    if not i.trigger or isinstance(walker, i.trigger):
                        if i.func:
                            walker.returns.append(i.func(current_node, warch))
                        else:
                            raise ValueError(f"No function {i.name} to call.")
                    if walker.disengaged:
                        return warch
        for i in warch._jac_exit_funcs_:
            if not i.trigger:
                if i.func:
                    walker.returns.append(i.func(warch, current_node))
                else:
                    raise ValueError(f"No function {i.name} to call.")
        walker.ignores = []
        return warch

    @staticmethod
    @hookimpl
    def destroy(obj: Architype | Anchor | BaseAnchor) -> None:
        """Destroy object."""
        if not FastAPI.is_enabled():
            return JacFeatureImpl.destroy(obj=obj)  # type:ignore[arg-type]

        anchor = obj.__jac__ if isinstance(obj, Architype) else obj

        if (
            isinstance(anchor, BaseAnchor)
            and anchor.state.deleted is None
            and Jac.check_write_access(anchor)  # type: ignore[arg-type]
        ):
            anchor.state.deleted = False
            match anchor:
                case NodeAnchor():
                    for edge in anchor.edges:
                        Jac.destroy(edge)
                case EdgeAnchor():
                    Jac.detach(anchor)
                case _:
                    pass

            Jac.get_context().mem.remove(anchor.id)
