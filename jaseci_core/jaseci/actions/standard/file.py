"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action
import json


@jaseci_action()
def load_str(fn: str, max_chars: int = None):
    """Standard built in for loading from file to string"""
    with open(fn, 'r') as file:
        data = file.read(max_chars)
    return data


@jaseci_action()
def load_json(fn: str):
    """Standard built in for loading json from file to dictionary"""
    with open(fn, 'r') as file:
        data = json.load(file)
    return data


@jaseci_action()
def dump_str(fn: str, s: str):
    """Standard built in for dumping to file from string"""
    with open(fn, 'w') as file:
        num_chars = file.write(s)
    return num_chars


@jaseci_action()
def append_str(fn: str, s: str):
    """Standard built in for appending to file from string"""
    with open(fn, 'a') as file:
        num_chars = file.write(s)
    return num_chars


@jaseci_action()
def dump_json(fn: str, obj, indent: int = None):
    """Standard built in for dumping json to file from dictionary"""
    with open(fn, 'w') as file:
        json.dump(obj, file, indent=indent)
