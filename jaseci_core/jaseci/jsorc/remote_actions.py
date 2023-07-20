"""
General action base class with automation for hot loading
"""
from jaseci.utils.utils import logger, ColCodes as Cc
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import validate_arguments
from time import time
import inspect
import uvicorn
import os
import re

var_args = re.compile(r"^\*[^\*]")
var_kwargs = re.compile(r"^\*\*[^\*]")

args_kwargs = (2, 4)
remote_actions = {}
registered_apis = []
registered_endpoints = []
ACTIONS_SPEC_LOC = "/jaseci_actions_spec/"
JS_ACTION_PREAMBLE = "js_action_"
JS_ENDPOINT_PREAMBLE = "js_endpoint_"


def mark_as_remote(api):
    registered_apis.append(api)


def mark_as_endpoint(endpoint):
    registered_endpoints.append(endpoint)


def serv_actions():
    """Returns fastAPI app interface for actions"""
    app = FastAPI(
        title="Jaseci Action Set API",
        description="A Jaseci Action Set",
    )

    @app.get("/")
    def home_redirect():
        return RedirectResponse(url="/docs")

    @app.get(ACTIONS_SPEC_LOC)
    def action_list():
        return remote_actions

    for i in registered_apis:
        gen_api_service(app, *i)
    for i in registered_endpoints:
        gen_endpoint(app, *i)
    return app


def gen_api_service(app, func, act_group, aliases, caller_globals):
    """Helper for jaseci_action decorator"""
    # Construct list of action apis available
    act_group = (
        [os.path.basename(inspect.getfile(func)).split(".")[0]]
        if act_group is None
        else act_group
    )
    varnames = []
    for param in inspect.signature(func).parameters.values():
        varnames.append(str(param) if param.kind in args_kwargs else param.name)

    remote_actions[f"{'.'.join(act_group+[func.__name__])}"] = varnames

    # Need to get pydatic model for func signature for fastAPI post
    model = validate_arguments(func).model

    # Keep only fields present in param list in base model
    keep_fields = {}
    for name in varnames:
        if var_args.match(name):
            keep_fields[name] = model.__fields__[name[1:]]
            keep_fields[name].name = name
            keep_fields[name].alias = name
        elif var_kwargs.match(name):
            keep_fields[name] = model.__fields__[name[2:]]
            keep_fields[name].name = name
            keep_fields[name].alias = name
        else:
            field = model.__fields__.get(name)
            if field:
                keep_fields[name] = field
    model.__fields__ = keep_fields

    # Create duplicate funtion for api endpoint and inject in call site globals
    @app.post(f"/{func.__name__}/")
    def new_func(params: model = model.construct()):
        params: dict = params.__dict__
        pl_peek = str(params)[:128]
        logger.info(str(f"Incoming call to {func.__name__} with {pl_peek}"))
        start_time = time()

        args = []
        kwargs = {}
        fp1 = inspect.signature(func).parameters.values()
        fp2 = list(fp1)

        # try to process args
        for param in fp1:
            _param = str(param) if param.kind in args_kwargs else param.name
            if _param in params:
                fp2.remove(param)
                if var_args.match(_param):
                    for arg in params.get(_param) or []:
                        args.append(arg)
                    break
                elif var_kwargs.match(_param):
                    kwargs.update(params.get(_param) or {})
                    break
                args.append(params.get(_param))
            else:
                break

        # try to process kwargs
        for param in fp2:
            param = str(param) if param.kind in args_kwargs else param.name
            if param in params:
                if var_kwargs.match(param):
                    kwargs.update(params.get(param) or {})
                    break
                kwargs[param] = params.get(param)
            else:
                break

        ret = validate_arguments(func)(*args, **kwargs)
        tot_time = time() - start_time
        logger.info(
            str(
                f"API call to {Cc.TG}{func.__name__}{Cc.EC}"
                f" completed in {Cc.TY}{tot_time:.3f} seconds{Cc.EC}"
            )
        )
        return ret

    if func.__name__ == "setup":
        new_func = app.on_event("startup")(new_func)
    for i in aliases:
        new_func = app.post(f"/{i}/")(new_func)
        remote_actions[f"{'.'.join(act_group+[i])}"] = varnames
    caller_globals[f"{JS_ACTION_PREAMBLE}{func.__name__}"] = new_func


def gen_endpoint(app, func, endpoint, mount, caller_globals):
    """Helper for jaseci_action decorator"""
    # Create duplicate funtion for api endpoint and inject in call site globals
    if mount is not None:
        app.mount(*mount)
    caller_globals[f"{JS_ENDPOINT_PREAMBLE}{func.__name__}"] = app.get(endpoint)(func)


def launch_server(port=80, host="0.0.0.0"):
    uvicorn.run(serv_actions(), port=port, host=host)
