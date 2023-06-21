"""
General action base class with automation for hot loading
"""
from importlib.util import spec_from_file_location, module_from_spec
from jaseci.utils.utils import logger, RXW1Lock
from jaseci.jsorc.remote_actions import ACTIONS_SPEC_LOC
from jaseci.jsorc.remote_actions import serv_actions, mark_as_remote, mark_as_endpoint
import requests
import multiprocessing
from queue import Empty
import os
import sys
import inspect
import importlib

# import threading
# import gc
import time

# import signal

# a = 1
# mutex = threading.Lock()
# MAX_WORKERS = 100
# actions_sem = Semaphore(MAX_WORKERS + 1)

ACTION_SUBPROC_TIMEOUT = 3  # 3 seconds

live_actions_lock = RXW1Lock()
live_actions = {}  # {"act.func": func_obj, ...}
live_action_modules = {}  # {__module__: ["act.func1", "act.func2", ...], ...}
action_configs = {}  # {"module_name": {}, ...}

act_procs = {}
glob_act_group = {}  # {"group_name": {"act_name": action, ...}, ...}
glob_act_hook = None


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


def load_local_actions(file: str, ctx: dict = {}):
    """Load all jaseci actions from python file"""
    try:
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
            try:
                if hasattr(mod, "setup"):
                    mod.setup(**ctx)
            except Exception as e:
                logger.error(
                    f"Cannot run set up for module {mod}. This could be because the module doesn't have a setup procedure for initialization, or wrong setup parameters are provided."
                )
                logger.error(e)
            return True
    except Exception as e:
        logger.error(f"Cannot hot load local actions from {file}: {e}")
        return False


def action_handler(mod, ctx, in_q, out_q, terminate_event):
    # Clearing the live actions in subprocess
    logger.info(f"clearing live_actions")
    live_actions.clear()
    logger.info(f"import_module on {mod}")
    loaded_mod = importlib.import_module(mod)
    logger.info(f"{mod} loaded")
    try:
        if hasattr(loaded_mod, "setup"):
            logger.info(f"call setup")
            loaded_mod.setup(**ctx)
    except Exception as e:
        logger.error(
            f"Cannot run set up for module {mod}.",
            " This could be because the module doesn't have a setup procedure for initialization, or wrong setup parameters are provided.",
        )
        logger.error(e)
    # logger.info(f"return list of actions")
    out_q.put(list(live_actions.keys()))

    while not terminate_event.is_set() or not in_q.empty():
        # while True:
        # logger.info(f"{os.getpid()} waiting on input")
        action, args, kwargs = in_q.get()
        try:
            # logger.info(f"{os.getpid()} Got input")
            func = live_actions[action]
            # logger.info(f"{os.getpid()}got func {func}")
            result = func(*args, **kwargs)
            # logger.info(f"{os.getpid()}got result")
        except Exception as e:
            logger.info(f"{os.getpid()}Exception: {str(e)}")
            result = str(e)

        out_q.put((action, result))
        # logger.info(f"{os.getpid()}put in out_q")


def action_handler_wrapper(name, *args, **kwargs):
    # module = action.split(".")[0]
    # name = action.split(".")[1]
    # logger.info(f"{os.getpid()}local action called for {name}")
    module = name.split(".")[0]
    act_name = name.split(".")[1]
    # TODO: temporary hack
    if module == "use" and act_name in [
        "encode",
        "text_similarity",
        "text_classify",
    ]:
        module = "use_enc"
    elif module == "use":
        module = "use_qa"

    module = f"jac_nlp.{module}"

    # logger.info("put in_q")
    act_procs[module]["reqs"] += 1
    # cnt = act_procs[module]["reqs"]
    # logger.info(f"{module} reqs: {cnt}")
    # logger.info(f"{os.getpid()}put in_q")
    act_procs[module]["in_q"].put((name, args, kwargs))

    # logger.info(f"{os.getpid()}waiting on out_q")
    # TODO: Handle concurrent calls?
    try:
        res = act_procs[module]["out_q"].get(timeout=ACTION_SUBPROC_TIMEOUT)[1]
    except Empty as e:
        logger.info(f"action subprocess out_q timeout {e}")
        logger.info(e)
        raise e
    except Exception as e:
        logger.info("Unknown exception caught.")
        raise e

    act_procs[module]["reqs"] -= 1
    cnt = act_procs[module]["reqs"]
    # logger.info(f"{module} reqs: {cnt}")

    return res


def load_module_actions(mod, loaded_module=None, ctx: dict = {}):
    # logger.info(f"load module actions {mod}")
    # If the module status is intialization, return False
    if mod in act_procs and act_procs[mod]["status"] == "INITIALIZATION":
        logger.info("already in initialization")
        return False

    # If the module is already loaded and not set as terminate, return True
    if (
        mod in act_procs
        and act_procs[mod]["status"] == "READY"
        and not act_procs[mod]["terminate_event"].is_set()
    ):
        # logger.info(f"already loaded and ready")
        return True

    # If module termination set to be True and no outstanding requests, we delete previously allocated queues and process
    if (
        mod in act_procs
        and act_procs[mod]["terminate_event"].is_set()
        and act_procs[mod]["reqs"] == 0
    ):
        # logger.info(f"clearing existing queues etc.")
        del act_procs[mod]["in_q"]
        del act_procs[mod]["out_q"]
        del act_procs[mod]["proc"]
        del act_procs[mod]

    # Create subprocess and message queues for this action module
    mp_ctx = multiprocessing.get_context("spawn")
    act_procs[mod] = {
        "in_q": mp_ctx.Queue(),
        "out_q": mp_ctx.Queue(),
        "terminate_event": mp_ctx.Event(),
        "reqs": 0,
        "status": "INITIALIZATION",
    }
    # logger.info(f"init the process")
    act_procs[mod]["proc"] = mp_ctx.Process(
        target=action_handler,
        args=(
            mod,
            ctx,
            act_procs[mod]["in_q"],
            act_procs[mod]["out_q"],
            act_procs[mod]["terminate_event"],
        ),
    )
    # logger.info(f"start the process")
    act_procs[mod]["proc"].start()

    # get the list of action back
    logger.info(f"waiting on list of actions")
    actions_list = act_procs[mod]["out_q"].get()

    # while actions_sem.acquire():
    #     # Only keep the semaphore if there are no other outstanding worker
    #     if actions_sem._value != MAX_WORKERS:
    #         actions_sem.release()
    #         continue
    #     else:
    #         break
    before_lock = time.time()
    live_actions_lock.writer_acquire()
    logger.info(f"live_actions_lock writer acquire in {time.time()-before_lock}")
    try:
        for act in actions_list:
            live_actions[act] = action_handler_wrapper
    finally:
        live_actions_lock.writer_release()
    logger.info(f"live_actions_lock writer release in {time.time()-before_lock}")
    # module intialization completes, set process status as ready
    act_procs[mod]["status"] = "READY"

    return True


# def load_module_actions(mod, loaded_module=None, ctx: dict = {}):
#     """Load all jaseci actions from python module"""
#     try:
#         if mod in sys.modules:
#             del sys.modules[mod]
#         if loaded_module and loaded_module in sys.modules:
#             del sys.modules[loaded_module]
#         if mod in live_action_modules:
#             for i in live_action_modules[mod]:
#                 if i in live_actions:
#                     del live_actions[i]
#         if loaded_module in live_action_modules:
#             for i in live_action_modules[loaded_module]:
#                 if i in live_actions:
#                     del live_actions[i]
#
#         mod = importlib.import_module(mod)
#         try:
#             if hasattr(mod, "setup"):
#                 mod.setup(**ctx)
#         except Exception as e:
#             logger.error(
#                 f"Cannot run set up for module {mod}. This could be because the module doesn't have a setup procedure for initialization, or wrong setup parameters are provided."
#             )
#             logger.error(e)
#         if mod:
#             return True
#     except Exception as e:
#         logger.error(f"Cannot hot load module actions from {mod}: {e}")
#
#     return False


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
    logger.info(f"{os.getpid()} Unloading {mod}")
    if mod in act_procs:
        # act_procs[mod]["proc"].kill()
        # act_procs[mod]["proc"].terminate()
        if act_procs[mod]["reqs"] > 0:
            # logger.info("Oustanding requests. Gracefully kill.")
            # logger.info("set event")
            act_procs[mod]["terminate_event"].set()
            # logger.info("joining")
            act_procs[mod]["proc"].join()
            # time.sleep(1)
            # logger.info("closing")
            act_procs[mod]["proc"].close()
            # logger.info("closed")
            del act_procs[mod]["in_q"]
            del act_procs[mod]["out_q"]
            del act_procs[mod]
            return True
        else:
            # logger.info("No outstanding requests. Kill now.")
            # logger.info("set event")
            # act_procs[mod]["terminate_event"].set()
            # logger.info("kill")
            act_procs[mod]["proc"].kill()
            # logger.info("joining")
            act_procs[mod]["proc"].join()
            # act_procs[mod]["proc"].terminate()
            # logger.info("closing")
            act_procs[mod]["proc"].close()
            # logger.info("closed")
            del act_procs[mod]["in_q"]
            del act_procs[mod]["out_q"]
            del act_procs[mod]
            # logger.info("Process closed")
        return True
    else:
        return False


# def unload_module(mod):
#     """Unload actions module and all relevant function"""
#     if mod in sys.modules.keys() and mod in live_action_modules.keys():
#         for i in live_action_modules[mod]:
#             if i in live_actions:
#                 del live_actions[i]
#
#         # Iterate through the objects in the module __dict__ to manually delete them
#         loaded_mod = sys.modules[mod]
#         mod_content_len = len(loaded_mod.__dict__)
#         for _ in range(mod_content_len):
#             mod_obj = loaded_mod.__dict__.pop(list(loaded_mod.__dict__.keys())[0])
#             del mod_obj
#         del loaded_mod
#         del sys.modules[mod]
#         del live_action_modules[mod]
#         gc.collect()
#         return True
#     return False


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
    from jaseci.prim.ability import Ability
    from jaseci.jsorc.memory import MemoryHook

    if not glob_act_group:
        glob_act_hook = MemoryHook()
        for i in live_actions.keys():
            name = i.split(".")
            if name[0] in [
                "std",
                "file",
                "net",
                "rand",
                "vector",
                "request",
                "date",
                "jaseci",
                "internal",
                "zip",
                "webtool",
                "url",
                "regex",
            ]:
                if name[0] not in glob_act_group:
                    glob_act_group[name[0]] = {}
                glob_act_group[name[0]][name[1]] = Ability(
                    m_id=0,
                    h=glob_act_hook,
                    mode="public",
                    name=i,
                    kind="ability",
                    value=i,
                    persist=False,
                )
    return glob_act_group


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


def load_remote_actions(url, ctx: dict = {}):
    """Load all jaseci actions from live pod"""
    headers = {"content-type": "application/json"}
    try:
        spec = requests.get(url.rstrip("/") + ACTIONS_SPEC_LOC, headers=headers)
        spec = spec.json()
        before_lock = time.time()
        live_actions_lock.writer_acquire()
        logger.info(
            f"live_actions_lock writer acquire in {time.time()-before_lock} Sec"
        )
        try:
            for i in spec.keys():
                live_actions[i] = gen_remote_func_hook(url, i, spec[i])
                if i.endswith(".setup") and ctx:
                    try:
                        live_actions[i](**ctx)
                    except Exception as e:
                        logger.error(
                            f"Cannot run set up for remote action {i}. This could be because the module doesn't have a setup procedure for initialization, or wrong setup parameters are provided."
                        )
                        logger.error(e)
        finally:
            live_actions_lock.writer_release()
        logger.info(
            f"live_actions_lock writer release in {time.time()-before_lock} Sec"
        )
        return True

    except Exception as e:
        logger.error(f"Cannot hot load remote actions at {url}: {e}")
        return False


def gen_remote_func_hook(url, act_name, param_names):
    """Generater for function calls for remote action calls"""

    def func(*args, **kwargs):
        params = {}
        for i in range(len(param_names)):
            if i < len(args):
                params[param_names[i]] = args[i]
            else:
                params[param_names[i]] = None
        for i in kwargs.keys():
            if i in param_names:
                params[i] = kwargs[i]
        # Remove any None-valued parameters to use the default value of the action def
        params = dict([(k, v) for k, v in params.items() if v is not None])
        act_url = f"{url.rstrip('/')}/{act_name.split('.')[-1]}"
        res = requests.post(
            act_url, headers={"content-type": "application/json"}, json=params
        )
        return res.json()

    func.__module__ = "js_remote_hook"

    return func


def call_action(action_name: str, ctx: dict = {}) -> None:
    """
    Call an action by name
    """
    try:
        action_name = action_name.strip()
        if action_name in live_actions.keys():
            res = live_actions[action_name](**ctx)
            return res, True
        else:
            raise Exception(f"Action {action_name} not found")
    except Exception as e:
        logger.error(f"Error calling action {action_name}: {e}")
        return None, False
