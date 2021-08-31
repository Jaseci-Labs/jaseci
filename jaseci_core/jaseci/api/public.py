from jaseci.actor.walker import walker
from jaseci.graph.node import node
from jaseci.element import element
from jaseci.utils.utils import logger, is_jsonable
from inspect import signature, getdoc
import uuid


class public_api():
    """
    Public  APIs
    """

    def __init__(self, hook):
        """
        self.committer is set by api implementaiton if intent
        is to commit changes enacted by public call
        """
        self.committer = None
        self.hook = hook

    def general_interface_to_api(self, params, api_name):
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
            param_map[i] = p_default if p_default is not \
                func_sig.parameters[i].empty else None
            if (p_name in params.keys()):
                val = params[p_name]
                if (issubclass(p_type, element)):
                    if(val is None or val == 'None'):
                        logger.error(
                            f'No {p_type} value for {p_name} provided!')
                    val = self.hook.get_obj(
                        'override', uuid.UUID(val), override=True)
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
            return signature(getattr(public_api, api_name))

    def get_api_doc(self, api_name):
        """
        Checks for valid api name and returns signature
        """
        if (not hasattr(self, api_name)):
            logger.error(f'{api_name} not a valid API')
            return False
        else:
            doc = getdoc(getattr(public_api, api_name))
            return doc

    def public_api_walker_summon(self, key: str, walk: walker, nd: node,
                                 ctx: dict = {}):
        """
        Public api for running walkers, namespace key must be provided
        along with the walker id and node id
        """
        if(key not in walk.namespace_keys()):
            return ['Not authorized to execute this walker']
        wlk = walk.duplicate()
        wlk.refresh()
        wlk.prime(nd, prime_ctx=ctx)
        res = wlk.run()
        self.committer = wlk._h.get_obj(wlk._m_id, uuid.UUID(wlk._m_id))
        wlk.destroy()
        return res
