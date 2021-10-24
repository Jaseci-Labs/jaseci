import requests


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
