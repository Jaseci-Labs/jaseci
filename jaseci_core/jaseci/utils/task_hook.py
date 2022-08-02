from multiprocessing import Process
from .utils import logger
from celery import Celery

_task_hook = None
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
        global _task_hook
        _task_hook = Celery("celery")
        _task_hook.config_from_object(config)

    def __worker(self, quiet):
        Process(target=_task_hook.Worker(quiet=quiet).start).start()

    def __scheduler(self, quiet):
        Process(target=_task_hook.Beat(quiet=quiet).run).start()

    def __tasks(self, *args):
        global _task_map
        for arg in args:
            if arg.__name__ not in _task_map:
                _task_map[arg.__name__] = _task_hook.register_task(arg())

    def queue(self, is_public=None):
        return _task_map["public_queue"] if is_public is None else _task_map["queue"]

    def dynamic_request(self):
        return _task_map["dynamic_request"]
