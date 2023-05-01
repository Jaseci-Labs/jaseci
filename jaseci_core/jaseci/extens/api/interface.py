"""
General master interface engine for client interfaces as mixin
"""
from inspect import signature, getdoc
from jaseci.utils.utils import logger, is_jsonable, is_true, exc_stack_as_str_list
from jaseci.prim.element import Element
from jaseci.prim.walker import Walker
import json


class Interface:
    """
    General master interface engine
    """

    _public_api = []
    _private_api = []
    _admin_api = []
    _cli_api = []

    def __init__(self):
        """
        self._pub_committer is set by api implementaiton if intent
        is to commit changes enacted by public call
        """
        self._pub_committer = None

    def assimilate_api(
        api_list,
        func,
        cmd_group=None,
        cli_args=None,
        url_args=None,
        allowed_methods=None,
    ):
        cmd_group = func.__name__.split("_") if cmd_group is None else cmd_group
        api_list.append(
            {
                "fname": func.__name__,
                "sig": signature(func),
                "doc": getdoc(func),
                "groups": cmd_group,
                "cli_args": cli_args if cli_args is not None else [],
                "url_args": url_args if url_args is not None else [],
                "allowed_methods": allowed_methods,
            }
        )
        return func

    def public_api(cmd_group=None, cli_args=None, url_args=None, allowed_methods=None):
        def decorator_func(func):
            return Interface.assimilate_api(
                Interface._public_api,
                func,
                cmd_group,
                cli_args,
                url_args,
                allowed_methods,
            )

        return decorator_func

    def private_api(cmd_group=None, cli_args=None, url_args=None, allowed_methods=None):
        def decorator_func(func):
            return Interface.assimilate_api(
                Interface._private_api,
                func,
                cmd_group,
                cli_args,
                url_args,
                allowed_methods,
            )

        return decorator_func

    def admin_api(cmd_group=None, cli_args=None, url_args=None, allowed_methods=None):
        def decorator_func(func):
            return Interface.assimilate_api(
                Interface._admin_api,
                func,
                cmd_group,
                cli_args,
                url_args,
                allowed_methods,
            )

        return decorator_func

    def cli_api(cmd_group=None, cli_args=None):
        def decorator_func(func):
            return Interface.assimilate_api(
                Interface._cli_api, func, cmd_group, cli_args
            )

        return decorator_func

    def all_apis(self, with_cli_only=False):
        ret = Interface._public_api + Interface._private_api + Interface._admin_api
        if with_cli_only:
            return ret + Interface._cli_api
        return ret

    assimilate_api = staticmethod(assimilate_api)
    public_api = staticmethod(public_api)
    private_api = staticmethod(private_api)
    admin_api = staticmethod(admin_api)
    cli_api = staticmethod(cli_api)

    def provide_internal_default(self, param):
        """
        Applies internal defaults for sentinel and graphs
        """
        if param == "snt" and self.active_snt_id:
            if self.active_snt_id == "global":
                glob_id = self._h.get_glob("GLOB_SENTINEL")
                if not glob_id:
                    return self.interface_error("No global sentinel is available!")
                else:
                    return glob_id
            return self.active_snt_id
        if param == "gph" or param == "nd":
            return (
                self.active_gph_id
                if self.active_gph_id
                else self.interface_error("No default graph node available!")
            )
        return None

    def interface_error(self, err, stack=None):
        """Standard error output to logger and api response"""
        logger.error(err)
        ret = {"response": err, "success": False, "errors": [err]}
        if stack:
            ret["stack_trace"] = stack
        return ret

    def general_interface_to_api(self, params, api_name):
        """
        A mapper utility to interface to master class
        Assumptions:
            params is a dictionary of parameter names and values in UUID
            api_name is the name of the api being mapped to
        """
        param_map = {}
        if (
            api_name.startswith("master_active")
            or api_name.startswith("master_become")
            or api_name.startswith("master_unbecome")
        ):
            _caller = self
        elif self.caller:
            _caller = self._h.get_obj(self._m_id, self.caller)
        else:
            _caller = self
        if not hasattr(_caller, api_name):
            return self.interface_error(f"{api_name} not a valid API")
        func_sig = signature(getattr(_caller, api_name))
        for i in func_sig.parameters.keys():
            if i == "self":
                continue
            p_name = i
            p_type = func_sig.parameters[i].annotation
            p_default = func_sig.parameters[i].default
            val = p_default if p_default is not func_sig.parameters[i].empty else None
            if p_name in params.keys():
                val = params[p_name]
            if val is None:  # Used to patch defaults
                val = _caller.provide_internal_default(p_name)
                if val is not None and "errors" in val:
                    return val
            if p_type == dict and isinstance(val, str):
                if not len(val):
                    val = {}
                else:
                    val = json.loads(val)
            if str(val) in _caller.alias_map.keys():
                val = _caller.alias_map[val]
            if issubclass(p_type, Element):
                if val is None:
                    break
                val = _caller._h.get_obj(_caller._m_id, val)
                if isinstance(val, p_type):
                    param_map[i] = self.sync_constraints(val, params)
                else:
                    return self.interface_error(f"{type(val)} is not {p_type}")
            else:  # TODO: Can do type checks here too
                param_map[i] = val

            if p_default and param_map[i] is None:
                return self.interface_error(f"Invalid API args - {params}")
        try:
            ret = getattr(_caller, api_name)(**param_map)
        except Exception as e:
            return self.interface_error(
                f"Internal Exception: {e}", stack=exc_stack_as_str_list()
            )
        if not is_jsonable(ret):
            return self.interface_error(f"Non-JSON API ret {type(ret)}: {ret}")
        return ret

    def public_interface_to_api(self, params, api_name):
        """
        A mapper utility to interface to public
        Assumptions:
            params is a dictionary of parameter names and values in UUID
            api_name is the name of the api being mapped to
        """
        param_map = {}
        if not hasattr(self, api_name):
            return self.interface_error(f"{api_name} not a valid API")
        func_sig = signature(getattr(self, api_name))
        for i in func_sig.parameters.keys():
            if i == "self":
                continue
            p_name = i
            p_type = func_sig.parameters[i].annotation
            p_default = func_sig.parameters[i].default
            val = p_default if p_default is not func_sig.parameters[i].empty else None
            if p_name in params.keys():
                val = params[p_name]
            if p_type == dict and isinstance(val, str):
                if not len(val):
                    val = {}
                else:
                    val = json.loads(val)
            if issubclass(p_type, Element):
                if val is None:
                    return self.interface_error(
                        f"No {p_type} value for {p_name} provided!"
                    )
                val = self._h.get_obj("override", val, override=True)
                self.seek_committer(val)
                if isinstance(val, p_type):
                    param_map[i] = self.sync_constraints(val, params)
                else:
                    return self.interface_error(f"{type(val)} is not {p_type}")
            else:  # TODO: Can do type checks here too
                param_map[i] = val

            if param_map[i] is None:
                return self.interface_error(f"Invalid API parameter set - {params}")
        try:
            ret = getattr(self, api_name)(**param_map)
        except Exception as e:
            return self.interface_error(
                f"Internal Exception: {e}", stack=exc_stack_as_str_list()
            )
        if not is_jsonable(ret):
            return self.interface_error(
                str(f"API returns non json object {type(ret)}: {ret}")
            )
        return ret

    # future constraints other than `async` should be add here
    def sync_constraints(self, obj, params):
        if isinstance(obj, Walker):
            obj.is_async = is_true(params.get("is_async", obj.is_async))

        return obj

    def seek_committer(self, obj):
        """Opportunistically assign a committer"""
        if not self._pub_committer and not (obj is None):
            self._pub_committer = obj._h.get_obj(obj._m_id, obj._m_id)

    def clear_committer(self):
        """Unset committer"""
        self._pub_committer = None
