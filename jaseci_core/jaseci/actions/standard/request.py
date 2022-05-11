"""Built in actions for Jaseci"""
import requests
from jaseci.actions.live_actions import jaseci_action
from base64 import b64decode, b64encode
from io import BytesIO


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
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
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
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
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
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
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
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
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
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
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
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
    return ret


@jaseci_action()
def multipart_base64(url: str, files: list, header: dict):
    """
    Issue request
    Param 1 - url
    Param 3 - header
    Param 3 - file (Optional) used for single file
    Param 4 - files (Optional) used for multiple files
    Note - file and files can't be None at the same time

    Return - response object
    """

    if not files:
        return {
            "status_code": 400,
            "error": "Please include base64 using this format "
            '{"field":val,"name":val,"base64":val} '
            "using parameter `file` and `files` for array file",
        }

    formData = []

    if files is not None:
        for f in files:
            formData.append(
                (
                    f["field"] if "field" in f else "file",
                    (f["name"], BytesIO(b64decode(f["base64"]))),
                )
            )

    res = requests.post(url, files=formData, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text
    return ret


@jaseci_action()
def file_download_base64(url: str, header: dict, encoding: str = "utf-8"):
    """Standard built in for download file from url"""
    with requests.get(url, stream=True, headers=header) as res:
        res.raise_for_status()
        with BytesIO() as buffer:
            for chunk in res.iter_content(chunk_size=8192):
                buffer.write(chunk)
            ret = buffer.getvalue()
    return b64encode(ret).decode(encoding)
