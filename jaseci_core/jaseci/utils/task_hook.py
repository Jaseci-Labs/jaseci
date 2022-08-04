import json
from multiprocessing import Process
from .utils import logger
from celery import Celery

from django_celery_results.models import TaskResult

_task_hook = None
_task_inspect = None
_proc_worker = None
_proc_scheduler = None
_task_map = {}


class task_hook:
    def __init__(self, config, *args, **kwargs):
        global _task_hook
        quiet = kwargs.get("quiet", False)

        if _task_hook is None:
            try:
                self.__celery(config)
                if _task_hook.control.inspect().ping() is None:
                    self.__tasks(*args)
                    self.__worker(quiet)
                    self.__scheduler(quiet)
            except Exception as e:
                logger.error(f"Resetting celery as it returns '{e}'")
                _task_hook = None

    def __celery(self, config):
        global _task_hook, _task_inspect
        _task_hook = Celery("celery")
        _task_hook.config_from_object(config)
        _task_inspect = _task_hook.control.inspect()

    def __worker(self, quiet):
        global _proc_worker
        _proc_worker = Process(target=_task_hook.Worker(quiet=quiet).start)
        _proc_worker.daemon = True
        _proc_worker.start()

    def __scheduler(self, quiet):
        global _proc_scheduler
        _proc_scheduler = Process(target=_task_hook.Beat(quiet=quiet).run)
        _proc_scheduler.daemon = True
        _proc_scheduler.start()

    def __tasks(self, *args):
        global _task_map
        for arg in args:
            if arg.__name__ not in _task_map:
                _task_map[arg.__name__] = _task_hook.register_task(arg())

    def inspect_tasks(self):
        return {
            "scheduled": _task_inspect.scheduled(),
            "active": _task_inspect.active(),
            "reserved": _task_inspect.reserved(),
        }

    def get_by_task_id(self, task_id):
        task = _task_hook.AsyncResult(task_id)

        res = {"state": task.state}

        if task.ready():
            task_result = TaskResult.objects.get(task_id=task_id).result
            try:
                res["result"] = json.loads(task_result)
            except ValueError as e:
                res["result"] = task_result

        return res

    def terminate_worker(self):
        _proc_worker.terminate()

    def terminate_scheduler(self):
        _proc_scheduler.terminate()

    def task_hook_ready(self):
        return not (_task_hook is None)

    def queue(self, is_public=None):
        return _task_map["public_queue"] if is_public is None else _task_map["queue"]

    def dynamic_request(self):
        return _task_map["dynamic_request"]
