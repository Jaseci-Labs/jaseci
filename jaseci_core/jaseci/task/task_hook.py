import json
import signal
import sys
from multiprocessing import Manager, Process
from uuid import UUID, uuid4

from jaseci.utils.app_state import AppState as AS

from ..utils.utils import logger
from .tasks import queue, scheduled_walker, scheduled_sequence
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
#                   TASK HOOK                   #
#################################################


class task_hook:

    app: Celery = None
    inspect = None
    worker = None
    scheduler = None
    state: AS = AS.NOT_STARTED
    quiet = False

    # --------------- REGISTERED TASK --------------- #
    queue = None
    scheduled_walker = None
    scheduled_sequence = None

    # ----------------- DATA SOURCE ----------------- #
    main_hook = None
    shared_mem = Manager().dict()

    # ------------------- MASTERS ------------------- #
    basic_master = None

    def __init__(self):

        if th.state.is_ready() and th.app is None:
            th.state = AS.STARTED

            th.main_hook = self

            try:
                self.__celery()

                if self.__inspect_ping():
                    self.__tasks()
                    self.__worker()
                    self.__scheduler()
                    th.state = AS.RUNNING
            except Exception as e:
                if not (th.quiet):
                    logger.error(
                        f"Skipping Celery due to initialization failure! Error: '{e}'"
                    )

                th.app = None
                th.state = AS.FAILED
                th.terminate_worker()
                th.terminate_scheduler()

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __celery(self):
        configs = self.get_task_config()
        enabled = configs.pop("enabled", True)

        if enabled:
            th.app = Celery("celery")
            th.quiet = configs.pop("quiet", False)
            th.app.conf.update(**configs)
            th.inspect = th.app.control.inspect()
        else:
            th.state = AS.DISABLED

    def __worker(self):
        th.worker = Process(target=th.app.Worker(quiet=th.quiet).start)
        th.worker.daemon = True
        th.worker.start()

    def __scheduler(self):
        th.scheduler = Process(target=th.app.Beat(quiet=th.quiet).run)
        th.scheduler.daemon = True
        th.scheduler.start()

    def __tasks(self):
        th.queue = th.app.register_task(queue())
        th.scheduled_walker = th.app.register_task(scheduled_walker())
        th.scheduled_sequence = th.app.register_task(scheduled_sequence())

    ###################################################
    #              COMMON GETTER/SETTER               #
    ###################################################

    def task_app(self):
        return th.app

    def task_running(self=None):
        return th.state == AS.RUNNING and not (th.app is None)

    def task_quiet(self, quiet=True):
        th.quiet = quiet

    def __inspect_ping(self):
        return not (th.inspect is None) and th.inspect.ping() is None

    # ---------------- QUEUE RELATED ---------------- #

    def inspect_tasks(self):
        return {
            "scheduled": th.inspect.scheduled(),
            "active": th.inspect.active(),
            "reserved": th.inspect.reserved(),
        }

    # --------------- ORM OVERRIDDEN ---------------- #
    def get_by_task_id(self, task_id):
        ret = {"status": "NOT_STARTED"}
        task = self.redis.get(f"{TASK_PREFIX}{task_id}")
        if task and "status" in task:
            ret["status"] = task["status"]
            if ret["status"] == "SUCESS":
                ret["result"] = task["result"]
        return ret

    ###################################################
    #                     QUEUING                     #
    ###################################################

    def get_element(jid):
        return th.main_hook.get_obj_from_store(UUID(jid))

    def add_queue(self, wlk, nd, *args):
        queue_id = str(uuid4())

        th.shared_mem.update(
            {queue_id: {"wlk": wlk.id.urn, "nd": nd.id.urn, "arg": args}}
        )
        return th.queue.delay(queue_id).task_id

    def consume_queue(queue_id):
        que = th.shared_mem.pop(queue_id)
        wlk = th.get_element(que["wlk"])
        nd = th.get_element(que["nd"])
        resp = wlk.run(nd, *que["arg"])
        wlk.destroy()

        return resp

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def terminate_worker(self=None):
        if not (th.worker is None):
            if not (th.quiet):
                logger.warn("Terminating task worker ...")
            th.worker.terminate()
            th.worker = None

    def terminate_scheduler(self=None):
        if not (th.scheduler is None):
            if not (th.quiet):
                logger.warn("Terminating task scheduler ...")
            th.scheduler.terminate()
            th.scheduler = None

    def task_reset(self):
        self.terminate_worker()
        self.terminate_scheduler()
        th.app = None
        th.inspect = None
        th.state = AS.NOT_STARTED
        task_hook.__init__(self)

    ###################################################
    #                     CONFIG                      #
    ###################################################

    # ORM_HOOK OVERRIDE
    def get_task_config(self):
        """Add celery config"""
        # disable scheduler on non django instance
        self.__scheduler = lambda: None
        return self.build_config("TASK_CONFIG", TASK_CONFIG)

    ###################################################
    #                  CLASS CONTROL                  #
    ###################################################

    def generate_basic_master():

        if th.basic_master is None:
            th.basic_master = task_hook.main_hook.generate_basic_master()

        return th.basic_master


# ----------------------------------------------- #

th = task_hook


###################################################
#                 PROCESS CLEANER                 #
###################################################

EXITING = False


def terminate_gracefully(sig, frame):
    global EXITING

    if not EXITING:
        EXITING = True
        th.terminate_worker()
        th.terminate_scheduler()
        logger.warn("Exitting gracefully ...")
        sys.exit(0)


signal.signal(signal.SIGINT, terminate_gracefully)
