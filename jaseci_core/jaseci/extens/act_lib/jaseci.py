"""Built in actions for Jaseci"""
from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import master_from_meta, copy_func
from jaseci.prim.super_master import SuperMaster
import functools


def interface_api(api_name, is_public, p_spec, *args, meta):
    """
    Interfaces Master apis after processing arguments/parameters
    from cli
    """
    mast = master_from_meta(meta)
    params = construct_params(p_spec, args)
    if is_public:
        return mast.public_interface_to_api(params, api_name)
    else:
        return mast.general_interface_to_api(params, api_name)


def construct_params(p_spec, args):
    arg_count = 0
    params = {}
    for i in p_spec.keys():
        if i == "self":
            continue
        p_default = (
            p_spec[i].default if p_spec[i].default is not p_spec[i].empty else None
        )
        if arg_count < len(args):
            params[i] = args[arg_count]
        else:
            params[i] = p_default
        arg_count += 1
    return params


def build_cmds():
    """
    Generates Click function with options for each command
    group and leaf signatures
    leaf is format: [api_name, func_sig, is_public, func_doc]
    """

    for i in SuperMaster.all_apis(None):
        func_name = "_".join(i["groups"])
        f = functools.partial(
            copy_func(interface_api, func_name),
            func_name,
            i in SuperMaster._public_api,
            i["sig"].parameters,
        )
        f.__name__ = func_name
        f.__doc__ = i["doc"]
        f.__module__ = __name__

        # original_args = inspect.getargspec(func).args
        globals()[func_name] = jaseci_action()(f)


build_cmds()
