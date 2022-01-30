"""
General action base class with automation for hot loading
"""
from hashlib import new
from jaseci.utils.utils import logger
from jaseci.actions.live_actions import live_actions
from fastapi import FastAPI
from pydantic import validate_arguments
from time import time
import inspect
import requests
import uvicorn
import os

remote_actions = {}
ACTIONS_SPEC_LOC = "/jaseci_actions_spec/"
JS_ACTION_PREAMBLE = "js_action_"
app = FastAPI()


@app.get(ACTIONS_SPEC_LOC)
def action_list():
    return remote_actions


def jaseci_action(act_group=None, aliases=list()):
    """Decorator for Jaseci Action interface"""
    caller_globals = dict(inspect.getmembers(
        inspect.stack()[1][0]))["f_globals"]
    if 'app' not in caller_globals:
        caller_globals['app'] = app

    def decorator_func(func):
        return assimilate_action(func, act_group, aliases, caller_globals)
    return decorator_func


def assimilate_action(func, act_group, aliases, caller_globals):
    """Helper for jaseci_action decorator"""
    # Construct list of action apis available
    act_group = [inspect.getfile(func).split(
        '.')[0]] if act_group is None else act_group
    remote_actions[f"{'.'.join(act_group+[func.__name__])}"] = \
        func.__code__.co_varnames

    # Need to get pydatic model for func signature for fastAPI post
    model = validate_arguments(func).model

    # Keep only feilds present in param list in base model
    keep_fields = {}
    for i in model.__fields__.keys():
        if i in func.__code__.co_varnames:
            keep_fields[i] = model.__fields__[i]
    model.__fields__ = keep_fields

    # Create duplicate funtion for api endpoint and inject in call site globals
    @app.post(f"/{func.__name__}/")
    def new_func(params: model):
        pl_peek = str(dict(params.__dict__))[:256]
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
            func.__code__.co_varnames
    caller_globals[f'{JS_ACTION_PREAMBLE}{func.__name__}'] = new_func

    # Return original function so it can be called as it in call site code base
    return func


def load_remote_actions(url):
    """Load all jaseci actions from live pod"""
    headers = {'content-type': 'application/json'}
    try:
        spec = requests.get(url.rstrip('/')+ACTIONS_SPEC_LOC,
                            headers=headers)
        spec = spec.json()
        for i in spec.keys():
            live_actions[i] = gen_remote_func_hook(url, i, spec[i])
        return True

    except Exception as e:
        logger.error(f"Cannot hot load remote actions at {url}: {e}")
        return False


def gen_remote_func_hook(url, act_name, param_names):
    """Generater for function calls for remote action calls"""
    def func(param_list, meta):
        params = {}
        for i in range(len(param_names)):
            if(i < len(param_list)):
                params[param_names[i]] = param_list[i]
            else:
                params[param_names[i]] = None
        act_url = f"{url.rstrip('/')}/{act_name.split('.')[-1]}"
        res = requests.post(
            act_url, headers={'content-type': 'application/json'}, json=params)
        return res.json()
    return func


def launch_server(port=80, host='0.0.0.0'):
    uvicorn.run(app, port=port, host=host)
