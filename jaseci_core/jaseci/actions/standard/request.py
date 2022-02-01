"""Built in actions for Jaseci"""
import requests
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def get(param_list, meta):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    url = param_list[0]
    data = param_list[1]
    header = param_list[2]
    res = requests.get(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def post(param_list, meta):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    url = param_list[0]
    data = param_list[1]
    header = param_list[2]
    res = requests.post(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def put(param_list, meta):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    url = param_list[0]
    data = param_list[1]
    header = param_list[2]
    res = requests.put(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def delete(param_list, meta):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    url = param_list[0]
    data = param_list[1]
    header = param_list[2]
    res = requests.delete(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def head(param_list, meta):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    url = param_list[0]
    data = param_list[1]
    header = param_list[2]
    res = requests.head(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def options(param_list, meta):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    url = param_list[0]
    data = param_list[1]
    header = param_list[2]
    res = requests.options(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret
