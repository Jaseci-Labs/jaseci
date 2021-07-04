"""
Main master handler for each user of Jaseci, serves as main interface between
between user and Jaseci
"""

import uuid
from inspect import signature
from inspect import getdoc


from jaseci.element import element

from jaseci.utils.utils import logger, is_jsonable
from jaseci.api.legacy import legacy_api
from jaseci.api.alias import alias_api
from jaseci.api.graph import graph_api
from jaseci.api.sentinel import sentinel_api
from jaseci.api.app import app_api
from jaseci.api.walker import walker_api
from jaseci.api.config import config_api


class master(element, legacy_api, alias_api, graph_api, sentinel_api,
             walker_api, app_api, config_api):
    """Main class for master functions for user"""

    def __init__(self, email="Anonymous", *args, **kwargs):
        element.__init__(self, name=email,
                         kind="Jaseci Master", *args, **kwargs)
        alias_api.__init__(self)
        graph_api.__init__(self)
        sentinel_api.__init__(self)

    def api_object_get(self, obj: element, detailed: bool = False):
        """
        Print the details of arbitrary jaseci object
        """
        return obj.serialize(detailed=detailed)

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        graph_api.destroy(self)
        sentinel_api.destroy(self)
        super().destroy()

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
                if(str(val) in self.alias_map.keys()):
                    val = self.alias_map[val]
                if (issubclass(p_type, element)):
                    val = self._h.get_obj(uuid.UUID(val))
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
            return signature(getattr(master, api_name))

    def get_api_doc(self, api_name):
        """
        Checks for valid api name and returns signature
        """
        if (not hasattr(self, api_name)):
            logger.error(f'{api_name} not a valid API')
            return False
        else:
            return getdoc(getattr(master, api_name))
