"""
General action base class with automation for hot loading
"""
from importlib.util import spec_from_file_location, module_from_spec
from jaseci.utils.utils import logger
from jaseci.actions.remote_actions import ACTIONS_SPEC_LOC
from jaseci.actions.remote_actions import serv_actions, mark_as_remote
import requests
import os
import sys
import inspect

live_actions = {}


def jaseci_action(act_group=None, aliases=list(), allow_remote=False):
    """Decorator for Jaseci Action interface"""
    caller_globals = dict(inspect.getmembers(
        inspect.stack()[1][0]))["f_globals"]
    if allow_remote and 'serv_actions' not in caller_globals:
        caller_globals['serv_actions'] = serv_actions

    def decorator_func(func):
        if(allow_remote):
            mark_as_remote([func, act_group, aliases, caller_globals])
        return assimilate_action(func, act_group, aliases)
    return decorator_func


def assimilate_action(func, act_group=None, aliases=list()):
    """Helper for jaseci_action decorator"""
    act_group = [func.__module__.split(
        '.')[-1]] if act_group is None else act_group
    live_actions[f"{'.'.join(act_group+[func.__name__])}"] = func
    for i in aliases:
        live_actions[f"{'.'.join(act_group+[i])}"] = func
    return func


def load_local_actions(file):
    """Load all jaseci actions from python file"""
    spec = spec_from_file_location(str(file).split("/")[-1][:-3], str(file))
    if(spec is None):
        logger.error(f"Cannot hot load from action file {file}")
        return False
    else:
        module_dir = os.path.dirname(os.path.realpath(str(file)))
        if module_dir not in sys.path:
            sys.path.append(module_dir)
        spec.loader.exec_module(module_from_spec(spec))
        return True


def load_standard():
    import jaseci.actions.standard.net  # noqa
    import jaseci.actions.standard.rand  # noqa
    import jaseci.actions.standard.request  # noqa
    import jaseci.actions.standard.std  # noqa
    import jaseci.actions.standard.file  # noqa
    import jaseci.actions.standard.vector  # noqa
    import jaseci.actions.standard.date  # noqa


load_standard()


def load_preconfig_actions(hook):
    import json
    action_preload = hook.resolve_glob('ACTION_SETS', None)
    if (action_preload):
        action_preload = json.loads(action_preload)
        for i in action_preload['local']:
            load_local_actions(i)
        for i in action_preload['remote']:
            load_remote_actions(i)


def get_global_actions(hook):
    """
    Loads all global action hooks for use by Jac programs
    Attaches globals to mem_hook
    """
    from jaseci.attr.action import action
    import uuid
    global_action_list = []
    for i in live_actions.keys():
        if(i.startswith('std.') or i.startswith('file.') or
           i.startswith('net.') or i.startswith('rand.') or
           i.startswith('vector.') or i.startswith('request.')):
            global_action_list.append(
                action(
                    m_id=uuid.UUID(int=0).urn,
                    h=hook,
                    mode='public',
                    name=i,
                    value=i,
                    persist=False
                ).jid
            )
    return global_action_list


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
    def func(*args):
        params = {}
        for i in range(len(param_names)):
            if(i < len(args)):
                params[param_names[i]] = args[i]
            else:
                params[param_names[i]] = None
        act_url = f"{url.rstrip('/')}/{act_name.split('.')[-1]}"
        res = requests.post(
            act_url, headers={'content-type': 'application/json'}, json=params)
        return res.json()
    return func
