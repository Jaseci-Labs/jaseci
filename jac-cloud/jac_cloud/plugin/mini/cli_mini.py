"""Module for registering CLI plugins for jaseci."""

from dataclasses import Field, MISSING, asdict, fields, is_dataclass
from inspect import isclass
from os import getenv, path
from pickle import load
from typing import Any, Type, cast, get_type_hints

from asyncer import syncify

from fastapi import APIRouter, Depends, FastAPI, File, Response, UploadFile, status
from fastapi.responses import ORJSONResponse

from jac_cloud.jaseci.utils import populate_yaml_specs

from jaclang import jac_import
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.architype import (
    Anchor,
    Architype,
    WalkerArchitype,
)
from jaclang.runtimelib.context import ExecutionContext
from jaclang.runtimelib.machine import JacMachine, JacProgram

from orjson import loads

from pydantic import BaseModel, Field as pyField, ValidationError, create_model

from starlette.datastructures import UploadFile as BaseUploadFile

from uvicorn import run

FILE_TYPES = {
    UploadFile,
    list[UploadFile],
    UploadFile | None,
    list[UploadFile] | None,
}


def response(reports: list[Any], status: int = 200) -> ORJSONResponse:
    """Return serialized version of reports."""
    resp: dict[str, Any] = {"status": status}

    for key, val in enumerate(reports):
        clean_response(key, val, reports)
    resp["reports"] = reports

    return ORJSONResponse(resp, status_code=status)


def clean_response(key: str | int, val: Any, obj: list | dict) -> None:  # noqa: ANN401
    """Cleanup and override current object."""
    match val:
        case list():
            for idx, lval in enumerate(val):
                clean_response(idx, lval, val)
        case dict():
            for key, dval in val.items():
                clean_response(key, dval, val)
        case Anchor():
            cast(dict, obj)[key] = asdict(val.report())
        case Architype():
            cast(dict, obj)[key] = asdict(val.__jac__.report())
        case val if is_dataclass(val) and not isinstance(val, type):
            cast(dict, obj)[key] = asdict(val)
        case _:
            pass


def gen_model_field(cls: type, field: Field, is_file: bool = False) -> tuple[type, Any]:
    """Generate Specs for Model Field."""
    if field.default is not MISSING:
        consts = (cls, pyField(default=field.default))
    elif callable(field.default_factory):
        consts = (cls, pyField(default_factory=field.default_factory))
    else:
        consts = (cls, File(...) if is_file else ...)

    return consts


def populate_apis(router: APIRouter, cls: Type[WalkerArchitype]) -> None:
    """Generate FastAPI endpoint based on WalkerArchitype class."""
    body: dict[str, Any] = {}
    files: dict[str, Any] = {}

    hintings = get_type_hints(cls)
    for f in fields(cls):
        f_name = f.name
        f_type = hintings[f_name]
        if f_type in FILE_TYPES:
            files[f_name] = gen_model_field(f_type, f, True)
        else:
            consts = gen_model_field(f_type, f)
            body[f_name] = consts

    payload: dict[str, Any] = {
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

        jctx = ExecutionContext.create(session=getenv("DATABASE", "database"))
        jctx.set_entry_node(node)

        Jac.spawn_call(cls(**body, **pl["files"]), jctx.entry_node.architype)
        jctx.close()

        return response(jctx.reports, getattr(jctx, "status", 200))

    def api_root(
        payload: payload_model = Depends(),  # type: ignore # noqa: B008
    ) -> Response:
        return api_entry(None, payload)

    router.post(url := f"/{cls.__name__}", summary=url)(api_root)
    router.post(url := f"/{cls.__name__}/{{node}}", summary=url)(api_entry)


def serve_mini(filename: str, host: str = "0.0.0.0", port: int = 8000) -> None:
    """Serve the jac application."""
    base, mod = path.split(filename)
    base = base if base else "./"
    mod = mod[:-4]

    if filename.endswith(".jac"):
        (module,) = jac_import(
            target=mod,
            base_path=base,
            cachable=True,
            override_name="__main__",
        )
    elif filename.endswith(".jir"):
        with open(filename, "rb") as f:
            JacMachine(base).attach_program(
                JacProgram(mod_bundle=load(f), bytecode=None)
            )
            (module,) = jac_import(
                target=mod,
                base_path=base,
                cachable=True,
                override_name="__main__",
            )
    else:
        JacMachine.detach()
        raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

    app = FastAPI()

    populate_yaml_specs(app)

    healtz_router = APIRouter(prefix="/healthz", tags=["monitoring"])
    walker_router = APIRouter(prefix="/walker", tags=["walker"])

    @healtz_router.get("", status_code=status.HTTP_200_OK)
    def healthz() -> Response:
        """Healthz API."""
        return Response()

    for obj in module.__dict__.values():
        if isclass(obj) and issubclass(obj, WalkerArchitype):
            populate_apis(walker_router, obj)

    app.include_router(healtz_router)
    app.include_router(walker_router)

    run(app, host=host, port=port)

    JacMachine.detach()
