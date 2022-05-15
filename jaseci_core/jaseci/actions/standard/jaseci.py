"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action
from jaseci.utils.utils import master_from_meta, copy_func
from jaseci.element.super_master import super_master
import functools


def interface_api(api_name, is_public, p_names, *args, meta):
    """
    Interfaces Master apis after processing arguments/parameters
    from cli
    """
    mast = master_from_meta(meta)
    params = {}
    if "self" in p_names:
        p_names.remove("self")
    for i in range(len(args)):
        if i < len(p_names):
            params[p_names[i]] = args[i]
    if is_public:
        return mast.public_interface_to_api(params, api_name)
    else:
        return mast.general_interface_to_api(params, api_name)


def build_cmds():
    """
    Generates Click function with options for each command
    group and leaf signatures
    leaf is format: [api_name, func_sig, is_public, func_doc]
    """

    for i in super_master.all_apis(None):
        func_name = "_".join(i["groups"])
        f = functools.partial(
            copy_func(interface_api, func_name),
            func_name,
            i in super_master._public_api,
            list(i["sig"].parameters.keys()),
        )
        f.__name__ = func_name
        f.__doc__ = i["doc"]
        f.__module__ = __name__

        # original_args = inspect.getargspec(func).args
        globals()[func_name] = jaseci_action()(f)


build_cmds()
