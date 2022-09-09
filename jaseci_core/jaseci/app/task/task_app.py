import signal
import sys
from multiprocessing import Manager, Process
from uuid import UUID, uuid4
from jaseci.app.common_app import common_app
from jaseci.utils.app_state import AppState as AS
from jaseci.utils.utils import logger
from .task_common import task_properties, queue, scheduled_walker, scheduled_sequence
from celery import Celery

################################################
#                   DEFAULTS                   #
################################################

TASK_PREFIX = "celery-task-meta-"
TASK_CONFIG = {
    "enabled": True,
    "quiet": False,
    "broker_url": "redis://localhost:6379/1",
    "result_backend": "redis://localhost:6379/1",
    "broker_connection_retry_on_startup": True,
    "task_track_started": True,
}


#################################################
#                   TASK APP                   #
#################################################


class task_app(common_app, task_properties):

    shared_mem = Manager().dict()

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        common_app.__init__(self, task_app)
        task_properties.__init__(self, self.cls)

        if self.is_ready():
            self.state = AS.STARTED

            try:
                self.__task(hook)
            except Exception:
                if not (self.quiet):
                    logger.exception("Skipping Celery due to initialization failure!")

                self.app = None
                self.state = AS.FAILED
                self.terminate_worker()
                self.terminate_scheduler()

    def __task(self, hook):
        configs = self.get_config(hook)
        enabled = configs.pop("enabled", True)

        if enabled:
            self.app = Celery("celery")
            self.quiet = configs.pop("quiet", False)
            self.app.conf.update(**configs)
            self.inspect = self.app.control.inspect()

            if self.ping():
                self.__tasks()
                self.__worker()
                self.__scheduler()
                self.state = AS.RUNNING
        else:
            self.state = AS.DISABLED

    def __worker(self):
        self.worker = Process(target=self.app.Worker(quiet=self.quiet).start)
        self.worker.daemon = True
        self.worker.start()

    def __scheduler(self):
        self.scheduler = Process(target=self.app.Beat(quiet=self.quiet).run)
        self.scheduler.daemon = True
        self.scheduler.start()

    def __tasks(self):
        self.queue = self.app.register_task(queue())
        self.scheduled_walker = self.app.register_task(scheduled_walker())
        self.scheduled_sequence = self.app.register_task(scheduled_sequence())

    ###################################################
    #              COMMON GETTER/SETTER               #
    ###################################################

    def ping(self):
        return not (self.inspect is None) and self.inspect.ping() is None

    # ---------------- QUEUE RELATED ---------------- #

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

    def consume_queue(wlk, nd, args, hook):
        wlk = hook.get_obj_from_store(UUID(wlk))
        nd = hook.get_obj_from_store(UUID(nd))
        resp = wlk.run(nd, *args)
        wlk.destroy()

        return resp

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

    def get_by_task_id(self, task_id, hook):
        ret = {"status": "NOT_STARTED"}
        task = hook.redis.get(f"{TASK_PREFIX}{task_id}")
        if task and "status" in task:
            ret["status"] = task["status"]
            if ret["status"] == "SUCESS":
                ret["result"] = task["result"]
        return ret

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
