"""Jaseci API Implementations."""

from dataclasses import Field, MISSING, fields, is_dataclass
from os import getenv
from re import compile
from types import NoneType
from typing import Any, Callable, Type, TypeAlias, Union, cast, get_type_hints

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

from jaclang.plugin.feature import JacFeature as Jac

from orjson import loads

from pydantic import BaseModel, Field as pyField, ValidationError, create_model

from starlette.datastructures import UploadFile as BaseUploadFile

from .websocket import websocket_events
from ...core.architype import NodeAnchor, WalkerAnchor, WalkerArchitype
from ...core.context import ContextResponse, JaseciContext
from ...jaseci.security import authenticator

# from ..jaseci.utils import log_entry, log_exit

DISABLE_AUTO_ENDPOINT = getenv("DISABLE_AUTO_ENDPOINT") == "true"
PATH_VARIABLE_REGEX = compile(r"{([^\}]+)}")
FILE_TYPES = {
    UploadFile,
    list[UploadFile],
    UploadFile | None,
    list[UploadFile] | None,
}

walker_router = APIRouter(prefix="/walker", tags=["walker"])


class DefaultSpecs:
    """Default API specs."""

    path: str = ""
    methods: list[str] = ["post"]
    as_query: str | list[str] = []
    excluded: str | list[str] = []
    auth: bool = True
    private: bool = False


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
        message: dict[str, Any] = {}

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
                        message[f_name] = files[f_name] = gen_model_field(
                            f_type, f, True
                        )
                    else:
                        consts = gen_model_field(f_type, f)
                        message[f_name] = consts

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

            # log = log_entry(
            #     cls.__name__,
            #     user.email if (user := getattr(request, "_user", None)) else None,
            #     pl,
            #     node,
            # )

            if isinstance(body, BaseUploadFile) and body_model:
                body = loads(syncify(body.read)())
                try:
                    body = body_model(**body).__dict__
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
                # log_exit(resp, log)

                return ORJSONResponse(resp, jctx.status)
            else:
                error = {
                    "error": f"You don't have access on target entry {jctx.entry_node.ref_id}!"
                }
                jctx.close()

                # log_exit(error, log)
                raise HTTPException(403, error)

        def api_root(
            request: Request,
            payload: payload_model = Depends(),  # type: ignore # noqa: B008
        ) -> Response:
            return api_entry(request, None, payload)

        for method in methods:
            method = method.lower()
            walker_method = getattr(walker_router, method)

            match method:
                case "websocket":
                    websocket_events[cls.__name__] = {
                        "type": cls,
                        "model": create_model(
                            f"{cls.__name__.lower()}_message_model", **message
                        ),
                        "auth": auth,
                    }
                case _:
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

                    walker_method(
                        url := f"/{cls.__name__}{path}", summary=url, **settings
                    )(api_root)
                    walker_method(
                        url := f"/{cls.__name__}/{{node}}{path}",
                        summary=url,
                        **settings,
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
