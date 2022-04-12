"""
General master interface engine for client interfaces as mixin
"""
import uuid
from inspect import signature, getdoc
from jaseci.utils.utils import logger
from jaseci.utils.utils import is_jsonable
from jaseci.element.element import element


class interface():
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

    def assimilate_api(api_list, func, cmd_group=None,
                       cli_args=None, url_args=None):
        cmd_group = func.__name__.split(
            '_') if cmd_group is None else cmd_group
        api_list.append(
            {'fname': func.__name__, 'sig': signature(func),
             'doc': getdoc(func), 'groups': cmd_group,
             'cli_args': cli_args if cli_args is not None else [],
             'url_args': url_args if url_args is not None else [], })
        return func

    def public_api(cmd_group=None, cli_args=None, url_args=None):
        def decorator_func(func):
            return interface.assimilate_api(
                interface._public_api, func, cmd_group, cli_args, url_args)
        return decorator_func

    def private_api(cmd_group=None, cli_args=None, url_args=None):
        def decorator_func(func):
            return interface.assimilate_api(
                interface._private_api, func, cmd_group, cli_args, url_args)
        return decorator_func

    def admin_api(cmd_group=None, cli_args=None, url_args=None):
        def decorator_func(func):
            return interface.assimilate_api(
                interface._admin_api, func, cmd_group, cli_args, url_args)
        return decorator_func

    def cli_api(cmd_group=None, cli_args=None):
        def decorator_func(func):
            return interface.assimilate_api(
                interface._cli_api, func, cmd_group, cli_args)
        return decorator_func

    def all_apis(self):
        return interface._public_api+interface._private_api + \
            interface._admin_api

    assimilate_api = staticmethod(assimilate_api)
    public_api = staticmethod(public_api)
    private_api = staticmethod(private_api)
    admin_api = staticmethod(admin_api)
    cli_api = staticmethod(cli_api)

    def provide_internal_default(self, param):
        """
        Applies internal defaults for sentinel and graphs
        """
        if(param == 'snt' and self.active_snt_id):
            if(self.active_snt_id == 'global'):
                glob_id = self._h.get_glob('GLOB_SENTINEL')
                if(not glob_id):
                    return self.interface_error(
                        'No global sentinel is available!')
                else:
                    return glob_id
            return self.active_snt_id
        if(param == 'gph' or param == 'nd'):
            return self.active_gph_id if self.active_gph_id else \
                self.interface_error('No default graph node available!')
        return None

    def interface_error(self, err, stack=None):
        """Standard error output to logger and api response"""
        logger.error(err)
        ret = {'response': err, 'success': False, 'errors': [err]}
        if(stack):
            ret['stack_trace'] = stack
        return ret

    def general_interface_to_api(self, params, api_name):
        """
        A mapper utility to interface to master class
        Assumptions:
            params is a dictionary of parameter names and values in UUID
            api_name is the name of the api being mapped to
        """
        param_map = {}
        if(api_name.startswith('master_active')):
            _caller = self
        else:
            _caller = self._caller
        if (not hasattr(_caller, api_name)):
            return self.interface_error(f'{api_name} not a valid API')
        func_sig = signature(getattr(_caller, api_name))
        for i in func_sig.parameters.keys():
            if (i == 'self'):
                continue
            p_name = i
            p_type = func_sig.parameters[i].annotation
            p_default = func_sig.parameters[i].default
            val = p_default if p_default is not \
                func_sig.parameters[i].empty else None
            if (p_name in params.keys()):
                val = params[p_name]
            if(val is None):  # Used to patch defaults
                val = _caller.provide_internal_default(p_name)
                if(val is not None and 'errors' in val):
                    return val
            if(str(val) in _caller.alias_map.keys()):
                val = _caller.alias_map[val]
            if (issubclass(p_type, element)):
                if(val is None):
                    break
                val = _caller._h.get_obj(
                    _caller._m_id, uuid.UUID(val))
                if (isinstance(val, p_type)):
                    param_map[i] = val
                else:
                    return self.interface_error(
                        f'{type(val)} is not {p_type}')
            else:  # TODO: Can do type checks here too
                param_map[i] = val

            if (param_map[i] is None):
                return self.interface_error(f'Invalid API args - {params}')
        try:
            ret = getattr(_caller, api_name)(**param_map)
        except Exception as e:
            import traceback as tb
            return self.interface_error(
                f'Internal Exception: {e}', stack=tb.format_exc())
        if(not is_jsonable(ret)):
            return self.interface_error(f'Non-JSON API ret {type(ret)}: {ret}')
        return ret

    def public_interface_to_api(self, params, api_name):
        """
        A mapper utility to interface to public
        Assumptions:
            params is a dictionary of parameter names and values in UUID
            api_name is the name of the api being mapped to
        """
        param_map = {}
        if (not hasattr(self, api_name)):
            return self.interface_error(f'{api_name} not a valid API')
            return False
        func_sig = signature(getattr(self, api_name))
        for i in func_sig.parameters.keys():
            if (i == 'self'):
                continue
            p_name = i
            p_type = func_sig.parameters[i].annotation
            p_default = func_sig.parameters[i].default
            val = p_default if p_default is not \
                func_sig.parameters[i].empty else None
            if (p_name in params.keys()):
                val = params[p_name]
            if (issubclass(p_type, element)):
                if(val is None):
                    return self.interface_error(
                        f'No {p_type} value for {p_name} provided!')
                val = self._h.get_obj(
                    'override', uuid.UUID(val), override=True)
                self.seek_committer(val)
                if (isinstance(val, p_type)):
                    param_map[i] = val
                else:
                    return self.interface_error(f'{type(val)} is not {p_type}')
                    param_map[i] = None
            else:  # TODO: Can do type checks here too
                param_map[i] = val

            if (param_map[i] is None):
                return self.interface_error(
                    f'Invalid API parameter set - {params}')
        try:
            ret = getattr(self, api_name)(**param_map)
        except Exception as e:
            import traceback as tb
            return self.interface_error(
                f'Internal Exception: {e}', stack=tb.format_exc())
        if(not is_jsonable(ret)):
            return self.interface_error(
                str(f'API returns non json object {type(ret)}: {ret}'))
        return ret

    def seek_committer(self, obj):
        """Opportunistically assign a committer"""
        if(not self._pub_committer):
            self._pub_committer = obj._h.get_obj(
                obj._m_id, uuid.UUID(obj._m_id))

    def clear_committer(self):
        """Unset committer"""
        self._pub_committer = None

    def sync_walker_from_global_sent(self, wlk):
        """Checks for matching code ir between global and spawned walker"""
        glob_id = wlk._h.get_glob('GLOB_SENTINEL')
        if(glob_id):
            snt = wlk._h.get_obj(wlk._m_id, uuid.UUID(glob_id))
            glob_wlk = snt.walker_ids.get_obj_by_name(wlk.name)
            if(glob_wlk and glob_wlk.code_sig != wlk.code_sig):
                wlk.apply_ir(glob_wlk.code_ir)
