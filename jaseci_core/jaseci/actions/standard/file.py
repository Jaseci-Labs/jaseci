"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action
import os
import json
import base64


@jaseci_action()
def load_str(fn: str, max_chars: int = None):
    """Standard built in for loading from file to string"""
    with open(fn, "r") as file:
        data = file.read(max_chars)
    return data


@jaseci_action()
def load_json(fn: str):
    """Standard built in for loading json from file to dictionary"""
    with open(fn, "r") as file:
        data = json.load(file)
    return data


@jaseci_action()
def load_to_b64(fn: str):
    """Standard built in for loading binary from file to base64"""
    with open(fn, "rb") as file:
        data = base64.b64encode(file.read()).decode("ascii")
    return data


@jaseci_action()
def dump_str(fn: str, s: str):
    """Standard built in for dumping to file from string"""
    with open(fn, "w") as file:
        num_chars = file.write(s)
    return num_chars


@jaseci_action()
def dump_json(fn: str, obj, indent: int = None):
    """Standard built in for dumping json to file from dictionary"""
    with open(fn, "w") as file:
        json.dump(obj, file, indent=indent)


@jaseci_action()
def dump_from_b64(fn: str, b64: str):
    """Standard built in for dumping binary to file from from base64"""
    with open(fn, "wb") as file:
        file.write(base64.b64decode(b64.encode("ascii")))


@jaseci_action()
def append_str(fn: str, s: str):
    """Standard built in for appending to file from string"""
    with open(fn, "a") as file:
        num_chars = file.write(s)
    return num_chars


@jaseci_action()
def append_from_b64(fn: str, b64: str):
    """Standard built in for appending binary to file from from base64"""
    with open(fn, "ab") as file:
        file.write(base64.b64decode(b64.encode("ascii")))


@jaseci_action()
def delete(fn: str):
    """Standard built in for deleting a file"""
    if os.path.exists(fn):
        os.remove(fn)
        return True
    else:
        return False


@jaseci_action()
def new(name: str, content_type: str = None, field: str = None, meta: dict = {}):
    """temp"""
    from jaseci.utils.file_handler import FileHandler

    hook = meta["h"]
    return hook.add_file_handler(
        FileHandler(name=name, content_type=content_type, field=field)
    )


@jaseci_action()
def update(
    id: str,
    name: str = None,
    content_type: str = None,
    field: str = None,
    meta: dict = {},
):
    """temp"""
    file_handler = meta["h"].get_file_handler(id)
    if name:
        file_handler.name = name

    if content_type:
        file_handler.content_type = content_type

    if field:
        file_handler.field = field


@jaseci_action()
def read(id: str, offset: int = None, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).read(offset)


@jaseci_action()
def seek(id: str, offset: int, whence: int = 0, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).seek(offset, whence)


@jaseci_action()
def open(id: str, mode: str = "r", encoding: str = "utf-8", meta: dict = {}, **kwargs):
    """temp"""
    meta["h"].get_file_handler(id).open(mode, encoding, False, **kwargs)


@jaseci_action()
def is_open(id: str, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).is_open()


@jaseci_action()
def write(id: str, content: str, meta: dict = {}):
    """temp"""
    meta["h"].get_file_handler(id).write(content)


@jaseci_action()
def flush(id: str, meta: dict = {}):
    """temp"""
    meta["h"].get_file_handler(id).flush()


@jaseci_action()
def close(id: str, meta: dict = {}):
    """temp"""
    meta["h"].get_file_handler(id).close()


@jaseci_action()
def delete(id: str, meta: dict = {}):
    """temp"""
    meta["h"].get_file_handler(id).delete()


@jaseci_action()
def to_base64(id: str, offset: int = None, meta: dict = {}):
    """temp"""
    return meta["h"].get_file_handler(id).base64(offset)
