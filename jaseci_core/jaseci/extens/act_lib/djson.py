"""Built in actions for Jaseci"""
from jaseci.jsorc.live_actions import jaseci_action
from json import loads, dumps
from re import compile

internal = compile(r"\(([a-zA-Z0-9_\.\$]*?)\)")
full = compile(r"^\{\{([a-zA-Z0-9_\.\$\(\)]*?)\}\}$")
partial = compile(r"\{\{([a-zA-Z0-9_\.\$\(\)]*?)\}\}")


def convert_dict(value) -> dict:
    try:
        if isinstance(value, str):
            return loads(value)
        else:
            return dict(value)
    except:
        return "Error JSON loads!"


def convert_str(value) -> str:
    if isinstance(value, (dict, list)):
        return dumps(value)
    else:
        return "" if value == None else str(value)


def get_deep_value(keys: list[str], source, default):
    if len(keys) == 0:
        return source

    key = keys.pop(0)
    _type = type(source)
    if _type is dict and key in source:
        return get_deep_value(keys, source[key], default)
    elif _type is list and key.isnumeric():
        return get_deep_value(keys, source[int(key)], default)
    else:
        return default


def get_value(jpath: str, source, default=None):
    while internal.search(jpath):
        for intern in internal.findall(jpath):
            jpath = jpath.replace(
                "(" + intern + ")", convert_str(get_value(intern, source, ""))
            )

    if jpath:
        keys = jpath.split(".")
        key = keys.pop(0)
        if key == "$":
            if isinstance(source, (dict, list)):
                return get_deep_value(keys, source, default)
            elif len(keys) == 0:
                return source
        elif key == "$s":
            if isinstance(source, (dict, list)):
                return convert_str(get_deep_value(keys, source, default))
            elif len(keys) == 0:
                return convert_str(source)
        elif key == "$i":
            if isinstance(source, (dict, list)):
                value = get_deep_value(keys, source, default)
                return 0 if value == None else int(value)
            elif len(keys) == 0:
                return 0 if source == None else int(source)
        elif key == "$d":
            if isinstance(source, (dict, list)):
                return convert_dict(get_deep_value(keys, source, default))
            elif len(keys) == 0:
                return convert_dict(source)
        else:
            pass
            # for future syntax
    return default


def parse_str(key: str, value: str, target, source):
    matcher = full.match(value)
    if matcher:
        value = get_value(matcher.group(1), source)
    else:
        for jpath in partial.findall(value):
            value = value.replace(
                "{{" + jpath + "}}", convert_str(get_value(jpath, source, ""))
            )

    if key:
        target[key] = value
    else:
        return value


def traverse_dict(target: dict, source):
    for key in target.keys():
        traverse(key, target[key], target, source)


def traverse_list(target: list, source):
    for key, value in enumerate(target):
        traverse(key, value, target, source)


def traverse(key, value, target, source):
    _type = type(value)
    if _type is dict:
        traverse_dict(value, source)
    elif _type is list:
        traverse_list(value, source)
    elif _type is str:
        parse_str(key, value, target, source)


@jaseci_action()
def parse(source, target):
    """
    Dynamic parsing of target dict or list

    Return - parsed target object
    """
    _type = type(target)
    if _type is dict:
        traverse_dict(target, source)
    elif _type is list:
        traverse_list(target, source)
    elif _type is str:
        return parse_str(None, target, None, source)

    return target
