"""Built in actions for Jaseci"""
import requests
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def get(url: str, data: dict, header: dict):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.get(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def post(url: str, data: dict, header: dict):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.post(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def put(url: str, data: dict, header: dict):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.put(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def delete(url: str, data: dict, header: dict):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.delete(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def head(url: str, data: dict, header: dict):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.head(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret


@jaseci_action()
def options(url: str, data: dict, header: dict):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.options(url, json=data, headers=header)
    ret = {'status_code': res.status_code}
    try:
        ret['response'] = res.json()
    except Exception:
        ret['response'] = res.text
    return ret
