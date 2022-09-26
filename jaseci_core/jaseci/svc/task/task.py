import signal
import sys
from multiprocessing import Process

from celery import Celery
from celery.backends.base import DisabledBackend

from jaseci.svc import CommonService, ServiceState as Ss
from jaseci.utils.utils import logger
from .common import Queue, ScheduledSequence, ScheduledWalker, TaskProperties

################################################
#                   DEFAULTS                   #
################################################

TASK_CONFIG = {
    "enabled": True,
    "quiet": True,
    "broker_url": "redis://localhost:6379/1",
    "result_backend": "redis://localhost:6379/1",
    "broker_connection_retry_on_startup": True,
    "task_track_started": True,
}


#################################################
#                   TASK APP                   #
#################################################


class TaskService(CommonService, TaskProperties):

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        CommonService.__init__(self, TaskService)
        TaskProperties.__init__(self, self.cls)

        try:
            if self.is_ready() and self.__has_redis(hook):
                self.state = Ss.STARTED
                self.__task(hook)
        except Exception as e:
            if not (self.quiet):
                logger.error(
                    "Skipping Celery due to initialization failure!\n"
                    f"{e.__class__.__name__}: {e}"
                )

            self.app = None
            self.state = Ss.FAILED
            self.terminate_worker()
            self.terminate_scheduler()

    def __task(self, hook):
        configs = self.get_config(hook)
        enabled = configs.pop("enabled", True)

        if enabled:
            self.quiet = configs.pop("quiet", False)
            self.app = Celery("celery")
            self.app.conf.update(**configs)
            self.inspect = self.app.control.inspect()
            self.__ping()
            self.__tasks()
            self.__worker()
            self.__scheduler()
            self.state = Ss.RUNNING
        else:
            self.state = Ss.DISABLED

    def __worker(self):
        self.worker = Process(target=self.app.Worker(quiet=self.quiet).start)
        self.worker.daemon = True
        self.worker.start()

    def __scheduler(self):
        self.scheduler = Process(target=self.app.Beat(quiet=self.quiet).run)
        self.scheduler.daemon = True
        self.scheduler.start()

    def __tasks(self):
        self.queue = self.app.register_task(Queue())
        self.scheduled_walker = self.app.register_task(ScheduledWalker())
        self.scheduled_sequence = self.app.register_task(ScheduledSequence())

    def __has_redis(self, hook=None):
        if not (hook is None) and hook.redis.has_failed():
            if not (self.quiet):
                logger.error(
                    "Redis is not yet running reason "
                    "for skipping Celery initialization!"
                )
            self.state = Ss.FAILED
            return False
        return True

    def __ping(self):  # will throw exception
        self.inspect.ping()
        self.app.AsyncResult("").result

    ###################################################
    #              COMMON GETTER/SETTER               #
    ###################################################

    def get_by_task_id(self, task_id, wait=False):
        task = self.app.AsyncResult(task_id)

        if isinstance(task.backend, DisabledBackend):
            return {
                "status": "DISABLED",
                "result": "result_backend is set to disabled!",
            }

        ret = {"status": task.state}
        if task.ready():
            ret["result"] = task.result
        elif wait:
            ret["result"] = task.get(disable_sync_subtasks=False)

        return ret

    def inspect_tasks(self):
        return {
            "scheduled": self.inspect.scheduled(),
            "active": self.inspect.active(),
            "reserved": self.inspect.reserved(),
        }

    ###################################################
    #                     QUEUING                     #
    ###################################################

    def add_queue(self, wlk, nd, *args):
        return self.queue.delay(wlk.id.urn, nd.id.urn, args).task_id

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def terminate_worker(self=None):
        if not (self.worker is None):
            if not (self.quiet):
                logger.warn("Terminating task worker ...")
            self.worker.terminate()
            self.worker = None

    def terminate_scheduler(self=None):
        if not (self.scheduler is None):
            if not (self.quiet):
                logger.warn("Terminating task scheduler ...")
            self.scheduler.terminate()
            self.scheduler = None

    def reset(self, hook):
        self.terminate_worker()
        self.terminate_scheduler()
        self.inspect = None
        self.build(hook)

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def get_config(self, hook) -> dict:
        self.__scheduler = lambda: None
        return hook.build_config("TASK_CONFIG", TASK_CONFIG)


# ----------------------------------------------- #


###################################################
#                 PROCESS CLEANER                 #
###################################################


def terminate_gracefully(*args):
    sys.exit(0)


signal.signal(signal.SIGINT, terminate_gracefully)
