"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action
from jaseci.utils.utils import master_from_meta, copy_func
import functools


def interface_api(api_name, is_public, meta, **kwargs):
    """
    Interfaces Master apis after processing arguments/parameters
    from cli
    """
    mast = master_from_meta(meta)
    if is_public:
        return mast.public_interface_to_api(kwargs, api_name)
    else:
        return mast.general_interface_to_api(kwargs, api_name)


def build_cmds():
    """
    Generates Click function with options for each command
    group and leaf signatures
    leaf is format: [api_name, func_sig, is_public, func_doc]
    """
    from jaseci.element.super_master import super_master

    for i in super_master.all_apis(None):
        func_name = "_".join(i["groups"])
        f = functools.partial(
            copy_func(interface_api, func_name),
            api_name=func_name,
            is_public=i in super_master._public_api,
        )
        f.__name__ = func_name
        f.__doc__ = i["doc"]
        f.__module__ = __name__

        globals()[func_name] = jaseci_action()(f)

        # func_sig = i["sig"]
        # for i in func_sig.parameters.keys():
        #     if i == "self":
        #         continue
        #     p_default = func_sig.parameters[i].default
        #     p_type = func_sig.parameters[i].annotation
        #     if p_type not in [int, bool, float]:
        #         p_type = str
        #     if i in cli_args:
        #         f = click.argument(f"{i}", type=p_type)(f)
        #     elif p_default is not func_sig.parameters[i].empty:
        #         f = click.option(
        #             f"-{i}", default=p_type(p_default), required=False, type=p_type
        #         )(f)
        #     else:
        #         f = click.option(f"-{i}", required=True, type=p_type)(f)
        # # to file option to dump response to a file
        # f = click.option(
        #     "--output",
        #     "-o",
        #     default="",
        #     required=False,
        #     type=str,
        #     help="Filename to dump output of this command call.",
        # )(f)
        # return group_func.command()(f)


build_cmds()
