from django.urls import path
from .views import AbstractJacAPIView
from .views import AbstractAdminJacAPIView, AbstractPublicJacAPIView
from jaseci.prim.element import Element
from jaseci_serv.base.models import SuperMaster
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
        if i == "self":
            continue
        p_name = i
        p_type = fsig.parameters[i].annotation
        if issubclass(p_type, Element):
            params.append(f"> {p_name}: UUID pointing to {p_type.__name__} object\n")
            json_samp[p_name] = uuid.uuid4().urn
        else:
            params.append(f"> {p_name}: type {p_type.__name__}\n")
            json_samp[p_name] = p_type()
            if p_type == str:
                json_samp[p_name] = "some string"
    if params:
        doc += "\n**Parameters**:\n"
        for i in params:
            doc += i
        doc += "\n**JSON Example**\n"
        doc += f"```javascript\n{json.dumps(json_samp, indent=4)}\n```\n"
    return doc


def rest_api_build_methods(api, view_cls, fname, apidocstr, func_sig):
    gen_cls = type(fname, (view_cls,), {})
    allowed_methods = (
        getattr(gen_cls, "http_method_names")
        if api["allowed_methods"] is None
        else api["allowed_methods"]
    )
    setattr(gen_cls, "http_method_names", allowed_methods)
    for method in allowed_methods:
        setattr(gen_cls, method, copy_func(getattr(gen_cls, method)))
        getattr(gen_cls, method).__doc__ = (
            api["doc"] + "\n\n" + rest_api_auto_doc(apidocstr, func_sig)
        )
    return gen_cls


generated_urls = []


def generate_apis(api_list, view_cls, dir_head):
    """
    Auto generates Django APIs based on core interface
    """
    for i in api_list:
        fname = "_".join(i["groups"])
        apidocstr = f"{dir_head}/{fname}"

        globals()[fname] = rest_api_build_methods(
            i, view_cls, fname, apidocstr, i["sig"]
        )

        global generated_urls
        url_args = ""
        for j in i["url_args"]:
            url_args += f"/<str:{j}>"
        generated_urls.append(
            path(apidocstr + url_args, globals()[fname].as_view(), name=fname)
        )


generate_apis(SuperMaster._public_api, AbstractPublicJacAPIView, "js_public")
generate_apis(SuperMaster._private_api, AbstractJacAPIView, "js")
generate_apis(SuperMaster._admin_api, AbstractAdminJacAPIView, "js_admin")
