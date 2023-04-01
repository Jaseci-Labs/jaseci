"""Built in actions for Jaseci"""
from jaseci.jsorc.live_actions import jaseci_action
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
