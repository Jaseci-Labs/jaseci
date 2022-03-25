"""
General action base class with automation for hot loading
"""
from jaseci.utils.utils import logger
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import validate_arguments
from time import time
import inspect
import uvicorn
import os

remote_actions = {}
registered_apis = []
ACTIONS_SPEC_LOC = "/jaseci_actions_spec/"
JS_ACTION_PREAMBLE = "js_action_"


def mark_as_remote(api):
    registered_apis.append(api)


def serv_actions():
    """Returns fastAPI app interface for actions"""
    app = FastAPI()
    @app.get("/")
    def home_redirect():
        return RedirectResponse(url='/docs')

    @app.get(ACTIONS_SPEC_LOC)
    def action_list():
        return remote_actions

    for i in registered_apis:
        gen_api_service(app, i[0], i[1], i[2], i[3])
    return app


def gen_api_service(app, func, act_group, aliases, caller_globals):
    """Helper for jaseci_action decorator"""
    # Construct list of action apis available
    varnames = list(inspect.signature(func).parameters.keys())
    act_group = [os.path.basename(inspect.getfile(func)).split(
        '.')[0]] if act_group is None else act_group
    remote_actions[f"{'.'.join(act_group+[func.__name__])}"] = \
        varnames

    # Need to get pydatic model for func signature for fastAPI post
    model = validate_arguments(func).model

    # Keep only feilds present in param list in base model
    keep_fields = {}
    for i in model.__fields__.keys():
        if i in varnames:
            keep_fields[i] = model.__fields__[i]
    model.__fields__ = keep_fields

    # Create duplicate funtion for api endpoint and inject in call site globals
    @app.post(f"/{func.__name__}/")
    def new_func(params: model):
        pl_peek = str(dict(params.__dict__))[:128]
        logger.info(str(
            f'Incoming call to {func.__name__} with {pl_peek}'))
        start_time = time()
        TY = '\033[33m'
        TG = '\033[32m'
        EC = '\033[m'  # noqa
        ret = validate_arguments(func)(**(params.__dict__))
        tot_time = time()-start_time
        logger.info(str(
            f'API call to {TG}{func.__name__}{EC}'
            f' completed in {TY}{tot_time:.3f} seconds{EC}'))
        return ret
    for i in aliases:
        new_func = app.post(f"/{i}/")(new_func)
        remote_actions[f"{'.'.join(act_group+[i])}"] = \
            varnames
    caller_globals[f'{JS_ACTION_PREAMBLE}{func.__name__}'] = new_func


def launch_server(port=80, host='0.0.0.0'):
    uvicorn.run(serv_actions(), port=port, host=host)
