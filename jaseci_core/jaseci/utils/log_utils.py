import re
from typing import List, Dict


def match_date(line: str) -> str:
    """Extracts the date from a log line"""
    matched = re.match(r"\d\d\d\d-\d\d-\d\d\ \d\d:\d\d:\d\d", line)
    if matched:
        return matched.group()

    return None


def match_level(line: str) -> str:
    """Extracts the level from a log line"""
    matched = re.search(r"-\s(ERROR|WARNING|INFO|DEBUG)\s-", line)
    if matched:
        [level] = matched.groups()
        return level

    return None


def parse_logs(logs: List[str]) -> List[Dict[str, str]]:
    """Convert log lines into an object with log metadata"""
    result = []
    for log in logs:
        date = match_date(log)
        level = match_level(log)
        result.append({"date": date, "level": level, "log": log})

    return result
