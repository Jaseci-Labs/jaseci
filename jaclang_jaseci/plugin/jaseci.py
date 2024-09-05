"""Jac Language Features."""

from collections import OrderedDict
from contextlib import suppress
from dataclasses import Field, MISSING, fields
from functools import wraps
from os import getenv
from re import compile
from typing import Any, Callable, Type, TypeVar, cast, get_type_hints

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

from jaclang.plugin.default import JacFeatureDefaults, hookimpl
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.architype import DSFunc

from orjson import loads

from pydantic import BaseModel, Field as pyField, ValidationError, create_model

from starlette.datastructures import UploadFile as BaseUploadFile

from ..core.architype import (
    Anchor,
    Architype,
    BaseAnchor,
    EdgeArchitype,
    GenericEdge,
    NodeAnchor,
    NodeArchitype,
    ObjectArchitype,
    Root,
    WalkerAnchor,
    WalkerArchitype,
)
from ..core.context import ExecutionContext, JaseciContext
from ..jaseci import FastAPI
from ..jaseci.security import authenticator


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
        as_query: str | list = specs.as_query or []
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
        for f in fields(cls):
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

            if isinstance(body, BaseUploadFile) and body_model:
                body = loads(syncify(body.read)())
                try:
                    body = body_model(**body).model_dump()
                except ValidationError as e:
                    return ORJSONResponse({"detail": e.errors()})

            jctx = JaseciContext.create(request, NodeAnchor.ref(node) if node else None)

            wlk: WalkerAnchor = cls(**body, **pl["query"], **pl["files"]).__jac__
            if jctx.validate_access():
                wlk.spawn_call(jctx.entry_node)
                jctx.close()
                return ORJSONResponse(jctx.response(wlk.returns))
            else:
                jctx.close()
                raise HTTPException(
                    403,
                    f"You don't have access on target entry{cast(Anchor, jctx.entry_node).ref_id}!",
                )

        def api_root(
            request: Request,
            payload: payload_model = Depends(),  # type: ignore # noqa: B008
        ) -> Response:
            return api_entry(request, None, payload)

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
    cls: Type[WalkerArchitype] | None = None,
    *,
    path: str = "",
    methods: list[str] = ["post"],  # noqa: B006
    as_query: str | list = [],  # noqa: B006
    auth: bool = True,
    private: bool = False,
) -> Callable:
    """Walker Decorator."""

    def wrapper(cls: Type[WalkerArchitype]) -> Type[WalkerArchitype]:
        if get_specs(cls) is None:
            p = path
            m = methods
            aq = as_query
            a = auth
            pv = private

            class __specs__(DefaultSpecs):  # noqa: N801
                path: str = p
                methods: list[str] = m
                as_query: str | list = aq
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
    auth: bool = True
    private: bool = False


class JacPlugin:
    """Jaseci Implementations."""

    @staticmethod
    @hookimpl
    def get_context() -> ExecutionContext:
        """Get current execution context."""
        if FastAPI.is_enabled():
            return JaseciContext.get()
        return JacFeatureDefaults.get_context()

    @staticmethod
    @hookimpl
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a new architype."""
        if FastAPI.is_enabled():
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
        return JacFeatureDefaults.make_architype(
            cls=cls, arch_base=arch_base, on_entry=on_entry, on_exit=on_exit
        )

    @staticmethod
    @hookimpl
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""
        if FastAPI.is_enabled():

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
        return JacFeatureDefaults.make_obj(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    @hookimpl
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""
        if FastAPI.is_enabled():

            def decorator(cls: Type[Architype]) -> Type[Architype]:
                """Decorate class."""
                cls = Jac.make_architype(
                    cls=cls, arch_base=NodeArchitype, on_entry=on_entry, on_exit=on_exit
                )
                return cls

            return decorator
        return JacFeatureDefaults.make_node(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    @hookimpl
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""
        if FastAPI.is_enabled():

            def decorator(cls: Type[Architype]) -> Type[Architype]:
                """Decorate class."""
                cls = Jac.make_architype(
                    cls=cls, arch_base=EdgeArchitype, on_entry=on_entry, on_exit=on_exit
                )
                return cls

            return decorator
        return JacFeatureDefaults.make_edge(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    @hookimpl
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""
        if FastAPI.is_enabled():

            def decorator(cls: Type[Architype]) -> Type[Architype]:
                """Decorate class."""
                cls = Jac.make_architype(
                    cls=cls,
                    arch_base=WalkerArchitype,
                    on_entry=on_entry,
                    on_exit=on_exit,
                )
                populate_apis(cls)
                return cls

            return decorator
        return JacFeatureDefaults.make_walker(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    @hookimpl
    def report(expr: Any) -> None:  # noqa:ANN401
        """Jac's report stmt feature."""
        if FastAPI.is_enabled():
            JaseciContext.get().reports.append(expr)
            return
        JacFeatureDefaults.report(expr=expr)

    @staticmethod
    @hookimpl
    def get_root() -> Root:
        """Jac's assign comprehension feature."""
        if FastAPI.is_enabled():
            return JaseciContext.get_root()
        return JacFeatureDefaults.get_root()  # type:ignore[return-value]

    @staticmethod
    @hookimpl
    def get_root_type() -> Type[Root]:
        """Jac's root getter."""
        if FastAPI.is_enabled():
            return Root
        return JacFeatureDefaults.get_root_type()  # type:ignore[return-value]

    @staticmethod
    @hookimpl
    def build_edge(
        is_undirected: bool,
        conn_type: Type[EdgeArchitype] | EdgeArchitype | None,
        conn_assign: tuple[tuple, tuple] | None,
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        if FastAPI.is_enabled():
            conn_type = conn_type if conn_type else GenericEdge

            def builder(source: NodeAnchor, target: NodeAnchor) -> EdgeArchitype:
                edge = conn_type() if isinstance(conn_type, type) else conn_type
                edge.__attach__(source, target, is_undirected)
                if conn_assign:
                    for fld, val in zip(conn_assign[0], conn_assign[1]):
                        if hasattr(edge, fld):
                            setattr(edge, fld, val)
                        else:
                            raise ValueError(f"Invalid attribute: {fld}")
                if source.persistent or target.persistent:
                    edge.__jac__.save()
                    target.save()
                    source.save()
                return edge

            return builder
        return JacFeatureDefaults.build_edge(  # type:ignore[return-value]
            is_undirected=is_undirected, conn_type=conn_type, conn_assign=conn_assign
        )

    @staticmethod
    @hookimpl
    def get_object(id: str) -> Architype | None:
        """Get object via reference id."""
        with suppress(ValueError):
            if isinstance(architype := BaseAnchor.ref(id).architype, Architype):
                return architype

        return None

    @staticmethod
    @hookimpl
    def object_ref(obj: Architype) -> str:
        """Get object reference id."""
        return str(obj.__jac__.ref_id)
