from .views import AbstractJacAPIView
from core.element import element
from core.master import master
from core.utils.mem_hook import mem_hook
from core.utils.utils import copy_func
from inspect import signature
import uuid
import json


def rest_api_auto_doc(endpoint: str, fsig: signature):
    """
    Automatically return string for REST Interface documentation
    Parameters include endpoint uri and signature
    """
    doc = f"**REST Endpoint**: {endpoint}\n"
    params = []
    json_samp = {}

    for i in fsig.parameters.keys():
        if (i == 'self'):
            continue
        p_name = i
        p_type = fsig.parameters[i].annotation
        if(issubclass(p_type, element)):
            params.append(
                f'> {p_name}: UUID pointing to {p_type.__name__} object\n')
            json_samp[p_name] = uuid.uuid4().urn
        else:
            params.append(f'> {p_name}: type {p_type.__name__}\n')
            json_samp[p_name] = p_type()
            if (p_type == str):
                json_samp[p_name] = 'some string'
    if (params):
        doc += f"\n**Parameters**:\n"
        for i in params:
            doc += i
        doc += f"\n**JSON Example**\n"
        doc += f"```javascript\n{json.dumps(json_samp, indent=4)}\n```\n"
    return doc


# Introspection on master interface to generate view class for master apis
for i in dir(master(h=mem_hook())):
    if (i.startswith('api_')):
        func_sig = signature(getattr(master, i))
        gen_cls = type(i,
                       (AbstractJacAPIView,),
                       {'api_sig': func_sig})
        gen_cls.post = copy_func(gen_cls.post)
        gen_cls.post.__doc__ = getattr(master, i).__doc__ + '\n\n' + \
            rest_api_auto_doc(f'/jac/{i[4:]}', func_sig)
        globals()[i] = gen_cls
