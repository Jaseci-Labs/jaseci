from .views import AbstractJacAPIView
from .views import AbstractAdminJacAPIView, AbstractPublicJacAPIView
from jaseci.element import element
from base.models import super_master
from jaseci.api.public_api import public_api
from jaseci.utils.mem_hook import mem_hook
from jaseci.utils.utils import copy_func
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
def generate_apis(M):
    for i in dir(M):
        if (i.startswith('api_')):
            cls = AbstractJacAPIView
            apidocstr = f'/jac/{i[4:]}'
        elif (i.startswith('admin_api_')):
            cls = AbstractAdminJacAPIView
            apidocstr = f'/admin/{i[10:]}'
        elif (i.startswith('public_api_')):
            cls = AbstractPublicJacAPIView
            apidocstr = f'/public/{i[11:]}'
        else:
            continue
        func_sig = M.get_api_signature(i)
        gen_cls = type(i,
                       (cls,),
                       {})
        gen_cls.post = copy_func(gen_cls.post)
        gen_cls.post.__doc__ = M.get_api_doc(i) + '\n\n' + \
            rest_api_auto_doc(apidocstr, func_sig)
        globals()[i] = gen_cls


generate_apis(super_master(h=mem_hook()))
generate_apis(public_api(None))
