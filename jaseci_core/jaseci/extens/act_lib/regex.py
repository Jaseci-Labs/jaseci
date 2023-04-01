import re

from jaseci.jsorc.live_actions import jaseci_action


def compile(pattern: str, flags=0):
    return re.compile(pattern=pattern, flags=flags)


@jaseci_action()
def findall(pattern: str, string: str, flags=0):
    return re.findall(pattern=pattern, string=string, flags=flags)


@jaseci_action()
def search(pattern: str, string: str, flags=0):
    m = re.search(pattern=pattern, string=string, flags=flags)
    if m:
        span = m.span()
        match = m.group()
        return {"span": span, "match": match}
    else:
        return None


@jaseci_action()
def match(pattern: str, string: str, flags=0):
    m = re.match(pattern=pattern, string=string, flags=flags)
    if m:
        span = m.span()
        match = m.group()
        return {"span": span, "match": match}
    else:
        return None


@jaseci_action()
def fullmatch(pattern: str, string: str, flags=0):
    m = re.fullmatch(pattern=pattern, string=string, flags=flags)
    if m:
        span = m.span()
        match = m.group()
        return {"span": span, "match": match}
    else:
        return None


@jaseci_action()
def split(pattern: str, string: str, maxsplit=0, flags=0):
    return re.split(pattern=pattern, string=string, maxsplit=maxsplit, flags=flags)


@jaseci_action()
def finditer(pattern: str, string: str, flags=0):
    iter = re.finditer(pattern, string, flags=0)
    ret_list = []
    for item in iter:
        dicta = {"span": item.span(), "match": item.group()}
        ret_list.append(dicta)

    return ret_list


@jaseci_action()
def sub(pattern: str, replace: str, string: str, count=0, flags=0):
    return re.sub(
        pattern=pattern, repl=replace, string=string, count=count, flags=flags
    )


@jaseci_action()
def subn(pattern: str, replace: str, string: str, count=0, flags=0):
    return list(
        re.subn(pattern=pattern, repl=replace, string=string, count=count, flags=flags)
    )


@jaseci_action()
def escape(pattern: str):
    return re.escape(pattern=pattern)


@jaseci_action()
def purge():
    return re.purge()
