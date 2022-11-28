import re


def match_date(line: str):
    matched = re.match(r"\d\d\d\d-\d\d-\d\d\ \d\d:\d\d:\d\d", line)
    if matched:
        return matched.group()

    return None


def match_level(line: str):
    matched = re.search(r"-\s(ERROR|WARNING|INFO|DEBUG)\s-", line)
    if matched:
        [level] = matched.groups()
        return level

    return None


def parse_logs(logs: list[str]):
    result = []
    for log in logs:
        date = match_date(log)
        level = match_level(log)
        result.append({"date": date, "level": level, "log": log})

    return result
