"""Built in actions for Jaseci"""
import requests
from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action()
def get(url: str, data: dict = {}, header: dict = {}):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.get(url, json=data, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
    return ret


@jaseci_action()
def post(url: str, data: dict = {}, header: dict = {}):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.post(url, json=data, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
    return ret


@jaseci_action()
def put(url: str, data: dict = {}, header: dict = {}):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.put(url, json=data, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
    return ret


@jaseci_action()
def delete(url: str, data: dict = {}, header: dict = {}):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.delete(url, json=data, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
    return ret


@jaseci_action()
def head(url: str, data: dict = {}, header: dict = {}):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.head(url, json=data, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
    return ret


@jaseci_action()
def options(url: str, data: dict = {}, header: dict = {}):
    """
    Issue request
    Param 1 - url
    Param 2 - data
    Param 3 - header

    Return - response object
    """
    res = requests.options(url, json=data, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
    return ret


@jaseci_action()
def multipart(
    url: str, data: dict = {}, files: list = [], header: dict = {}, meta: dict = {}
):
    """
    Issue request
    Param 1 - url
    Param 2 - data (Optional) used for request body
    Param 3 - files (Optional) used for request files
    Param 4 - header

    Return - response object
    """

    hook = meta["h"]

    if not files:
        return {
            "status_code": 400,
            "error": "Please include base64 using this format "
            '{"field":val,"name":val,"base64":val} '
            "using parameter `file` and `files` for array file",
        }

    _files = []
    stream_to_be_close = []

    if files is not None:
        for f in files:
            file_handler = hook.get_file_handler(f)
            stream = file_handler.open("rb", None, True)
            stream_to_be_close.append(stream)
            _files.append(
                (
                    file_handler.field or "file",
                    (file_handler.name, stream, file_handler.content_type),
                )
            )

    res = requests.post(url, data=data, files=_files, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text

    for stream in stream_to_be_close:
        stream.close()

    return ret
