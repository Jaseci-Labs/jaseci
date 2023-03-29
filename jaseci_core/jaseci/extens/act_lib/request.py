"""Built in actions for Jaseci"""
import requests
from jaseci.jsorc.live_actions import jaseci_action


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
def multipart(url: str, files: list, header: dict, meta: dict):
    """
    Issue request
    Param 1 - url
    Param 3 - header
    Param 3 - file (Optional) used for single file
    Param 4 - files (Optional) used for multiple files
    Note - file and files can't be None at the same time

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

    form_data = []

    stream_to_be_close = []

    if files is not None:
        for f in files:
            file_handler = hook.get_file_handler(f)
            stream = file_handler.open("rb", None, True)
            stream_to_be_close.append(stream)
            form_data.append(
                (
                    file_handler.field or "file",
                    (file_handler.name, stream, file_handler.content_type),
                )
            )

    res = requests.post(url, files=form_data, headers=header)
    ret = {"status_code": res.status_code}
    try:
        ret["response"] = res.json()
    except Exception:
        ret["response"] = res.text

    for stream in stream_to_be_close:
        stream.close()

    return ret


@jaseci_action()
def file_download(url: str, header: dict = {}, meta: dict = {}):
    """Standard built in for download file from url"""
    from jaseci.utils.file_handler import FileHandler

    tmp = FileHandler("tmp")
    meta["h"].add_file_handler(tmp)

    with requests.get(url, stream=True, headers=header) as res:
        res.raise_for_status()
        tmp.open(mode="wb", encoding=None)
        for chunk in res.iter_content(chunk_size=8192):
            tmp.buffer.write(chunk)
        tmp.close()

    return tmp.id
