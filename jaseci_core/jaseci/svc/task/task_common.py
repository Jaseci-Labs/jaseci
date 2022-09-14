import re
from copy import deepcopy
from multiprocessing import Process
from typing import Tuple
from uuid import UUID

from celery import Task
from celery.app.control import Inspect
from requests import get, post
from requests.exceptions import HTTPError

DEFAULT_MSG = "Skipping scheduled walker!"


class Queue(Task):
    def run(self, wlk, nd, args):
        from jaseci.svc import MetaService

        hook = MetaService().hook()

        wlk = hook.get_obj_from_store(UUID(wlk))
        nd = hook.get_obj_from_store(UUID(nd))
        resp = wlk.run(nd, *args)
        wlk.destroy()

        return resp


class ScheduledWalker(Task):
    def get_obj(self, jid):
        return self.hook.get_obj_from_store(UUID(jid))

    def run(self, name, ctx, nd=None, snt=None, mst=None):
        from jaseci.svc import MetaService

        self.hook = MetaService().hook()

        if mst:
            mst = self.get_obj(mst)
        else:
            return f"{DEFAULT_MSG} mst (Master) is required!"

        if mst is None:
            return f"{DEFAULT_MSG} Invalid Master!"

        try:
            if not snt:
                if mst.active_snt_id == "global":
                    global_snt_id = self.hook.get_glob("GLOB_SENTINEL")
                    snt = self.get_obj(global_snt_id)
                elif mst.active_snt_id:
                    snt = self.get_obj(mst.active_snt_id)
            elif snt in mst.alias_map:
                snt = self.get_obj(mst.alias_map[snt])
            else:
                snt = self.get_obj(snt)

            if not snt:
                return f"{DEFAULT_MSG} Invalid Sentinel!"

            if not nd:
                if mst.active_gph_id:
                    nd = self.get_obj(mst.active_gph_id)
            elif nd in mst.alias_map:
                nd = self.get_obj(mst.alias_map[nd])
            else:
                nd = self.get_obj(nd)

            if not nd:
                return f"{DEFAULT_MSG} Invalid Node!"

            return mst.walker_run(name, nd, ctx, ctx, snt, False, False)
        except Exception as e:
            return f"{DEFAULT_MSG} Error occured: {e}"


class ScheduledSequence(Task):
    json_escape = re.compile(r"[^a-zA-Z0-9_]")
    internal = re.compile(r"\(([a-zA-Z0-9_\.\[\]\$\#\@\!]*?)\)")
    full = re.compile(r"^\{\{([a-zA-Z0-9_\.\[\]\$\#\(\)\@\!]*?)\}\}$")
    partial = re.compile(r"\{\{([a-zA-Z0-9_\.\[\]\$\#\(\)\@\!]*?)\}\}")

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

    def trigger_interface(self, req: dict):
        from jaseci.svc import MetaService

        master = req.get("master")
        app = MetaService()
        if master is None:
            caller = app.master()
            trigger_type = "public"
        else:
            caller = app.hook().get_obj_from_store(master)
            trigger_type = "general"

        api = req.get("api")
        body = req.get("body", {})

        return getattr(caller, f"{trigger_type}_interface_to_api")(body, api)

    def run(self, *args, **kwargs):
        requests = kwargs.get("requests")
        persistence = kwargs.get("persistence", {})
        container = kwargs.get("container", {"current": persistence})
        index = container.get("index", "0")

        if "parent_current" in container:
            container["current"] = container["parent_current"]

        for req in requests:
            try:
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

                if method == "JAC":
                    container["current"] = self.trigger_interface(req)
                else:
                    if method == "POST":
                        response = post(
                            req["api"],
                            json=req.get("body", {}),
                            headers=req.get("header", {}),
                        )
                    elif method == "GET":
                        response = get(req["api"], headers=req.get("header", {}))
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

            if "break" in req and self.and_condition(
                (persistence, container["current"]), req["break"]
            ):
                break

        return persistence


c1 = Queue
c2 = ScheduledWalker
c3 = ScheduledSequence


class TaskProperties:
    def __init__(self, prop):
        if not hasattr(prop, "_inspect"):
            setattr(prop, "_inspect", None)
            setattr(prop, "_worker", None)
            setattr(prop, "_scheduler", None)

            # --------------- REGISTERED TASK --------------- #
            setattr(prop, "_queue", None)
            setattr(prop, "_scheduled_walker", None)
            setattr(prop, "_scheduled_sequence", None)

    @property
    def inspect(self) -> Inspect:
        return self.cls._inspect

    @inspect.setter
    def inspect(self, val: Inspect):
        self.cls._inspect = val

    @property
    def worker(self) -> Process:
        return self.cls._worker

    @worker.setter
    def worker(self, val: Process):
        self.cls._worker = val

    @property
    def scheduler(self) -> Process:
        return self.cls._scheduler

    @scheduler.setter
    def scheduler(self, val: Process):
        self.cls._scheduler = val

    @property
    def queue(self) -> c1:
        return self.cls._queue

    @queue.setter
    def queue(self, val: c1):
        self.cls._queue = val

    @property
    def scheduled_walker(self) -> c2:
        return self.cls._scheduled_walker

    @scheduled_walker.setter
    def scheduled_walker(self, val: c2):
        self.cls._scheduled_walker = val

    @property
    def scheduled_sequence(self) -> c3:
        return self.cls._scheduled_sequence

    @scheduled_sequence.setter
    def scheduled_sequence(self, val: c3):
        self.cls._scheduled_sequence = val
