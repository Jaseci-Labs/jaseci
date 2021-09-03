"""
General master interface engine for client interfaces as mixin
"""
import uuid
from inspect import signature
from inspect import getdoc
from jaseci.utils.utils import logger
from jaseci.utils.utils import is_jsonable
from jaseci.element import element


class interface():
    """
    General master interface engine
    """

    def provide_internal_default(self, param):
        """
        Applies internal defaults for sentinel and graphs
        """
        if(param == 'snt' and self.active_snt_id):
            return self.active_snt_id
        if(param == 'gph' and self.active_gph_id):
            return self.active_gph_id
        if(param == 'nd' and self.active_gph_id):
            return self.active_gph_id
        return 'None'  # Meke me more elegant one day

    def general_interface_to_api(self, params, api_name):
        """
        A mapper utility to interface to master class
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
            param_map[i] = p_default if p_default is not \
                func_sig.parameters[i].empty else None
            if (p_name in params.keys()):
                val = params[p_name]
                if(val is None or val == 'None'):  # Used to patch defaults
                    val = self.provide_internal_default(p_name)
                if(str(val) in self.alias_map.keys()):
                    val = self.alias_map[val]
                if (issubclass(p_type, element)):
                    if(val is None or val == 'None'):
                        logger.error(
                            f'No {p_type} value for {p_name} provided!')
                    val = self._h.get_obj(self._m_id, uuid.UUID(val))
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
        if (len(param_map) < len(params)-1):
            logger.warning(
                str(f'Unused parameters in API call - '
                    f'got {params.keys()}, expected {param_map.keys()}'))
        ret = getattr(self, api_name)(**param_map)
        if(not is_jsonable(ret)):
            logger.error(
                str(f'API returns non json object {type(ret)}: {ret}'))
        return ret

    def get_api_signature(self, api_name):
        """
        Checks for valid api name and returns signature
        """
        if (not hasattr(self, api_name)):
            logger.error(f'{api_name} not a valid API')
            return False
        else:
            return signature(getattr(self, api_name))

    def get_api_doc(self, api_name):
        """
        Checks for valid api name and returns signature
        """
        if (not hasattr(self, api_name)):
            logger.error(f'{api_name} not a valid API')
            return False
        else:
            doc = getdoc(getattr(self, api_name))
            # if(api_name in dir(legacy_api)):
            #     doc = "Deprecated!\n" + doc
            return doc
