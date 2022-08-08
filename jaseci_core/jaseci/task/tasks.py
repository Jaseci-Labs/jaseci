import re

from copy import deepcopy
from typing import Tuple
from requests import post, get
from requests.exceptions import HTTPError
from celery import Task


class queue(Task):
    def run(self, queue_id):
        from .task_hook import task_hook

        ret = task_hook.consume(queue_id)

        return ret


class dynamic_request(Task):
    json_escape = re.compile("[^a-zA-Z0-9_]")
    internal = re.compile("\(([a-zA-Z0-9_\.\[\]\$\#\@\!]*?)\)")
    full = re.compile("^\{\{([a-zA-Z0-9_\.\[\]\$\#\(\)\@\!]*?)\}\}$")
    partial = re.compile("\{\{([a-zA-Z0-9_\.\[\]\$\#\(\)\@\!]*?)\}\}")

    def get_deep_value(self, data, keys, default):
        if len(keys) == 0:
            return data

        key = keys.pop(0)
        t = type(data)

        if t is dict and key in data:
            return self.get_deep_value(data[key], keys, default)
        elif t is list and key.isnumeric():
            return self.get_deep_value(data[int(key)], keys, default)
        else:
            return default

    def get_value(self, holder: Tuple, keys: str, default=None):
        while self.internal.search(keys):
            for intern in self.internal.findall(keys):
                keys = keys.replace(
                    "(" + intern + ")", self.get_value(holder, intern, "")
                )

        if keys:
            keys = keys.split(".")
            key = keys.pop(0)
            if key == "#":
                return self.get_deep_value(holder[0], keys, default)
            elif key == "$":
                t = type(holder[1])
                if t is dict or t is list:
                    return self.get_deep_value(holder[1], keys, default)
                else:
                    return holder[1]
            elif key == "@":
                t = type(holder[2])
                if t is dict or t is list:
                    return self.get_deep_value(holder[2], keys, default)
                else:
                    return holder[2]
            elif key == "!":
                return holder[3]
        return default

    def compare(self, condition, expected, actual):
        if condition == "eq":
            return actual == expected
        elif condition == "ne":
            return actual != expected
        elif condition == "gt":
            return actual > expected
        elif condition == "gte":
            return actual >= expected
        elif condition == "lt":
            return actual < expected
        elif condition == "lte":
            return actual <= expected
        elif condition == "regex":
            return re.compile(expected).match(actual)

    def condition(self, holder: Tuple, filter):
        for cons in filter["condition"].keys():
            if not (filter["condition"][cons] is None) and not self.compare(
                cons, filter["condition"][cons], self.get_value(holder, filter["by"])
            ):
                return False
        return True

    def or_condition(self, holder: Tuple, filter):
        for filt in filter:
            if "condition" in filt and self.condition(holder, filt):
                return True
            elif "or" in filt and self.or_condition(holder, filt["or"]):
                return True
            elif "and" in filt and self.and_condition(holder, filt["and"]):
                return True
        return False

    def and_condition(self, holder: Tuple, filter):
        for filt in filter:
            if "condition" in filt and not self.condition(holder, filt):
                return False
            elif "or" in filt and not self.or_condition(holder, filt["or"]):
                return False
            elif "and" in filt and not self.and_condition(holder, filt["and"]):
                return False
        return True

    def deep_replace_str(self, holder: Tuple, data, key):
        matcher = self.full.match(data[key])
        if matcher:
            data[key] = self.get_value(holder, matcher.group(1))
        else:
            for rep in self.partial.findall(data[key]):
                data[key] = data[key].replace(
                    "{{" + rep + "}}", self.get_value(holder, rep, "")
                )

    def deep_replace_dict(self, holder: Tuple, data):
        for key in data.keys():
            if key != "__def_loop__":
                t = type(data[key])
                if t is str:
                    self.deep_replace_str(holder, data, key)
                elif t is dict:
                    self.deep_replace_dict(holder, data[key])

    def save(self, holder: Tuple, req, params):
        if params in req:
            holder[0][self.json_escape.sub("_", req[params])] = holder[1]

    def run(self, *args, **kwargs):
        requests = kwargs.get("requests")
        persistence = kwargs.get("persistence", {})
        container = kwargs.get("container", {})
        index = container.get("index", "0")

        if "parent_current" in container:
            container["current"] = container["parent_current"]

        for req in requests:
            try:
                if "current" in container:
                    self.deep_replace_dict(
                        (
                            persistence,
                            container["current"],
                            container.get("parent_current", {}),
                            index,
                        ),
                        req,
                    )
                self.save((persistence, req), req, "save_req_to")

                method = req["method"].upper()

                if method == "POST":
                    response = post(
                        req["url"],
                        json=req.get("body", {}),
                        headers=req.get("header", {}),
                    )
                elif method == "GET":
                    response = get(req["url"], headers=req.get("header", {}))

                response.raise_for_status()

                if "application/json" in response.headers.get("Content-Type"):
                    container["current"] = response.json()
                else:
                    container["current"] = response.text

                if "__def_loop__" in req:
                    def_loop = req["__def_loop__"]
                    for idx, loop in enumerate(
                        self.get_value(
                            (persistence, container["current"]), def_loop["by"], []
                        )
                    ):
                        if "filter" in def_loop and not self.and_condition(
                            (persistence, loop), def_loop["filter"]
                        ):
                            continue
                        loop_container = {"parent_current": loop, "index": str(idx)}
                        self.run(
                            requests=deepcopy(def_loop["requests"]),
                            persistence=persistence,
                            container=loop_container,
                        )

                self.save((persistence, container["current"]), req, "save_to")

            except Exception as err:
                container["current"] = (
                    {
                        "status": err.response.status_code,
                        "message": err.response.reason,
                    }
                    if isinstance(err, HTTPError)
                    else {
                        "worker_error": str(err),
                    }
                )

                self.save((persistence, container["current"]), req, "save_to")

                if "ignore_error" not in req or not req["ignore_error"]:
                    if "parent_current" in container:
                        raise err
                    break

        return persistence
