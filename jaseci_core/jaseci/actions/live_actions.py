"""
General action base class with automation for hot loading
"""
from importlib.util import spec_from_file_location, module_from_spec
from jaseci.utils.utils import logger
from jaseci.actions.remote_actions import ACTIONS_SPEC_LOC
from jaseci.actions.remote_actions import serv_actions, mark_as_remote, mark_as_endpoint
import requests
import os
import sys
import inspect
import importlib

live_actions = {}  # {"act.func": func_obj, ...}
live_action_modules = {}  # {__module__: ["act.func1", "act.func2", ...], ...}
action_configs = {}  # {"module_name": {}, ...}


def jaseci_action(act_group=None, aliases=list(), allow_remote=False):
    """Decorator for Jaseci Action interface"""
    caller_globals = dict(inspect.getmembers(inspect.currentframe().f_back))[
        "f_globals"
    ]
    if allow_remote and "serv_actions" not in caller_globals:
        caller_globals["serv_actions"] = serv_actions

    def decorator_func(func):
        if allow_remote:
            mark_as_remote([func, act_group, aliases, caller_globals])
        return assimilate_action(func, act_group, aliases)

    return decorator_func


def jaseci_expose(endpoint, mount=None):
    """Decorator for Jaseci Action interface"""
    caller_globals = dict(inspect.getmembers(inspect.currentframe().f_back))[
        "f_globals"
    ]
    if "serv_actions" not in caller_globals:
        caller_globals["serv_actions"] = serv_actions

    def decorator_func(func):
        mark_as_endpoint([func, endpoint, mount, caller_globals])
        return func

    return decorator_func


def assimilate_action(func, act_group=None, aliases=list()):
    """Helper for jaseci_action decorator"""
    act_group = [func.__module__.split(".")[-1]] if act_group is None else act_group
    action_name = f"{'.'.join(act_group+[func.__name__])}"
    live_actions[action_name] = func
    if func.__module__ != "js_remote_hook":
        if func.__module__ in live_action_modules:
            live_action_modules[func.__module__].append(action_name)
        else:
            live_action_modules[func.__module__] = [action_name]
    for i in aliases:
        live_actions[f"{'.'.join(act_group+[i])}"] = func
        if func.__module__ != "js_remote_hook":
            if func.__module__ in live_action_modules:
                live_action_modules[func.__module__].append(
                    f"{'.'.join(act_group+[i])}"
                )
            else:
                live_action_modules[func.__module__] = [f"{'.'.join(act_group+[i])}"]
    return func


def load_local_actions(file: str):
    """Load all jaseci actions from python file"""
    name = file.rstrip(".py")
    name = ".".join(name.split("/")[-2:])
    # Assumes parent folder of py file is a package for internal relative
    # imports, name is package.module and package path is added to sys path
    spec = spec_from_file_location(name, str(file))
    if spec is None:
        logger.error(f"Cannot hot load from action file {file}")
        return False
    else:
        module_dir = os.path.dirname(os.path.dirname(os.path.realpath(file)))
        if module_dir not in sys.path:
            sys.path.append(module_dir)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        return True


def load_module_actions(mod, loaded_module=None):
    """Load all jaseci actions from python module"""
    if mod in sys.modules:
        del sys.modules[mod]
    if loaded_module and loaded_module in sys.modules:
        del sys.modules[loaded_module]
    if mod in live_action_modules:
        for i in live_action_modules[mod]:
            if i in live_actions:
                del live_actions[i]
    if loaded_module in live_action_modules:
        for i in live_action_modules[loaded_module]:
            if i in live_actions:
                del live_actions[i]
    mod = importlib.import_module(mod)
    if mod:
        return True
    return False


def load_action_config(config, module_name):
    """
    Load the action config of a jaseci action module
    """

    loaded_configs = importlib.import_module(config).ACTION_CONFIGS
    if module_name and module_name in loaded_configs:
        action_configs[module_name] = loaded_configs[module_name]
        return True
    else:
        return False


def unload_module(mod):
    """Unload actions module and all relevant function"""
    if mod in sys.modules.keys() and mod in live_action_modules.keys():
        for i in live_action_modules[mod]:
            if i in live_actions:
                del live_actions[i]
        del sys.modules[mod]
        del live_action_modules[mod]
        return True
    return False


def unload_action(name):
    """Unload actions module and all relevant function"""
    if name in live_actions.keys():
        mod = live_actions[name].__module__
        if mod != "js_remote_hook":
            live_action_modules[mod].remove(name)
            if len(live_action_modules[mod]) < 1:
                unload_module(mod)
        del live_actions[name]
        return True
    return False


def unload_actionset(name):
    """Unload actions module and all relevant function"""
    act_list = []
    orig_len = len(live_actions)
    for i in live_actions.keys():
        if i.startswith(name + "."):
            act_list.append(i)
    for i in act_list:
        unload_action(i)
    return len(live_actions) != orig_len


def load_preconfig_actions(hook):
    import json

    action_preload = hook.resolve_glob("ACTION_SETS", None)
    if action_preload:
        try:
            action_preload = json.loads(action_preload)
            for i in action_preload["local"]:
                load_local_actions(i)
            for i in action_preload["remote"]:
                load_remote_actions(i)
            for i in action_preload["module"]:
                load_module_actions(i)
        except Exception:
            pass


def get_global_actions():
    """
    Loads all global action hooks for use by Jac programs
    Attaches globals to mem_hook
    """
    from jaseci.attr.action import Action
    from jaseci.hook.memory import MemoryHook

    global_action_list = []
    hook = MemoryHook()
    for i in live_actions.keys():
        if (
            i.startswith("std.")
            or i.startswith("file.")
            or i.startswith("net.")
            or i.startswith("rand.")
            or i.startswith("vector.")
            or i.startswith("request.")
            or i.startswith("date.")
            or i.startswith("jaseci.")
            or i.startswith("internal.")
            or i.startswith("zlib.")
            or i.startswith("webtool.")
        ):
            global_action_list.append(
                Action(
                    m_id=0,
                    h=hook,
                    mode="public",
                    name=i,
                    value=i,
                    persist=False,
                )
            )
    return global_action_list


def unload_remote_actions(url):
    """
    Get the list of actions from the given URL and then unload them.
    """
    headers = {"content-type": "application/json"}
    try:
        spec = requests.get(url.rstrip("/") + ACTIONS_SPEC_LOC, headers=headers)
        spec = spec.json()
        for i in spec.keys():
            unload_action(i)
        return True
    except Exception as e:
        logger.error(f"Cannot unload remote action from {url}: {e}")


def load_remote_actions(url):
    """Load all jaseci actions from live pod"""
    headers = {"content-type": "application/json"}
    try:
        spec = requests.get(url.rstrip("/") + ACTIONS_SPEC_LOC, headers=headers)
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
            if i < len(args):
                params[param_names[i]] = args[i]
            else:
                params[param_names[i]] = None
        act_url = f"{url.rstrip('/')}/{act_name.split('.')[-1]}"
        res = requests.post(
            act_url, headers={"content-type": "application/json"}, json=params
        )
        return res.json()

    func.__module__ = "js_remote_hook"

    return func
