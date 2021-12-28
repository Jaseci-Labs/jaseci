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

    def __init__(self):
        """
        self._pub_committer is set by api implementaiton if intent
        is to commit changes enacted by public call
        """
        self._pub_committer = None

    def public_api(func, cmd_group=None):
        cmd_group = func.__name__.split(
            '_') if cmd_group is None else cmd_group
        interface._public_api.append(
            {'fname': func.__name__, 'sig': signature(func),
             'doc': getdoc(func), 'groups': cmd_group})
        return func

    def private_api(func, cmd_group=None):
        cmd_group = func.__name__.split(
            '_') if cmd_group is None else cmd_group
        interface._private_api.append(
            {'fname': func.__name__, 'sig': signature(func),
             'doc': getdoc(func), 'groups': cmd_group})
        return func

    def admin_api(func, cmd_group=None):
        cmd_group = func.__name__.split(
            '_') if cmd_group is None else cmd_group
        interface._admin_api.append(
            {'fname': func.__name__, 'sig': signature(func),
             'doc': getdoc(func), 'groups': cmd_group})
        return func

    def all_apis(self):
        return self._public_api+self._private_api+self._admin_api

    public_api = staticmethod(public_api)
    private_api = staticmethod(private_api)
    admin_api = staticmethod(admin_api)

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
        if(param == 'gph' and self.active_gph_id):
            return self.active_gph_id
        if(param == 'nd' and self.active_gph_id):
            return self.active_gph_id
        return None

    def interface_error(self, err):
        """Standard error output to logger and api response"""
        logger.error(err)
        return {'response': err, 'success': False, 'errors': [err]}

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
                    # return self.interface_error(
                    #     f'No {p_type} value for {p_name} provided!')
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
        # if (len(param_map) < len(params)-1):
        #     logger.warning(
        #         str(f'Unused parameters in API call - '
        #             f'got {params.keys()}, expected {param_map.keys()}'))
        ret = getattr(_caller, api_name)(**param_map)
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
            logger.error(f'{api_name} not a valid API')
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
                    logger.error(
                        f'No {p_type} value for {p_name} provided!')
                val = self._h.get_obj(
                    'override', uuid.UUID(val), override=True)
                self.seek_committer(val)
                if (isinstance(val, p_type)):
                    param_map[i] = val
                else:
                    logger.error(f'{type(val)} is not {p_type}')
                    param_map[i] = None
            else:  # TODO: Can do type checks here too
                param_map[i] = val

            if (param_map[i] is None):
                logger.error(f'Invalid API parameter set - {params}')
                return False
        ret = getattr(self, api_name)(**param_map)
        if(not is_jsonable(ret)):
            logger.error(
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

    def get_api_signature(self, api_name):
        """
        Checks for valid api name and returns signature
        """
        if (not hasattr(self._caller, api_name)):
            logger.error(f'{api_name} not a valid API')
            return False
        else:
            return signature(getattr(self._caller, api_name))

    def get_api_doc(self, api_name):
        """
        Checks for valid api name and returns signature
        """
        if (not hasattr(self._caller, api_name)):
            logger.error(f'{api_name} not a valid API')
            return False
        else:
            doc = getdoc(getattr(self._caller, api_name))
            # if(api_name in dir(legacy_api)):
            #     doc = "Deprecated!\n" + doc
            return doc

    def sync_walker_from_global_sent(self, wlk):
        """Checks for matching code ir between global and spawned walker"""
        glob_id = wlk._h.get_glob('GLOB_SENTINEL')
        if(glob_id):
            snt = wlk._h.get_obj(wlk._m_id, uuid.UUID(glob_id))
            glob_wlk = snt.walker_ids.get_obj_by_name(wlk.name)
            if(glob_wlk and glob_wlk.code_sig != wlk.code_sig):
                wlk.apply_ir(glob_wlk.code_ir)
