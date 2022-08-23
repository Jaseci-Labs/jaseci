import signal
import sys
from multiprocessing import Manager, Process
from uuid import UUID, uuid4

from ..utils.utils import logger
from .tasks import queue, schedule_queue
from celery import Celery

################################################
# ----------------- DEFAULTS ----------------- #
################################################

QUIET = True
PREFIX = "celery-task-meta-"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
CELERY_DEFAULT_CONFIGS = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "broker_connection_retry_on_startup": True,
    "task_track_started": True,
}

#################################################
# ----------------- TASK HOOK ----------------- #
#################################################


class task_hook:

    app = None
    inspect = None
    worker = None
    scheduler = None
    # -1 Failed : 0 Not Started : 1 Running
    state = -1
    quiet = False

    # --------------- REGISTERED TASK --------------- #
    queue = None
    schedule_queue = None

    # ----------------- DATA SOURCE ----------------- #
    main_hook = None
    shared_mem = None

    def __init__(self):

        if th.state < 0 and th.app is None:
            th.state = 0

            th.main_hook = self

            try:
                self.__celery()

                if th.inspect.ping() is None:
                    self.__tasks()
                    self.__worker()
                    self.__scheduler()
                    th.state = 1
            except Exception as e:
                if not (th.quiet):
                    logger.error(
                        f"Skipping Celery due to initialization failure! Error: '{e}'"
                    )

                th.app = None
                th.terminate_worker()
                th.terminate_scheduler()

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __celery(self):
        th.app = Celery("celery")
        self.task_config()
        th.inspect = th.app.control.inspect()
        th.shared_mem = Manager().dict()

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
        th.schedule_queue = th.app.register_task(schedule_queue())

    ###################################################
    #              COMMON GETTER/SETTER               #
    ###################################################

    def task_app(self):
        return th.app

    def task_hook_ready(self):
        return th.state == 1 and not (th.app is None)

    def task_quiet(self, quiet=QUIET):
        th.quiet = quiet

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
        task = self.redis.get(f"{PREFIX}{task_id}")
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

    def terminate_worker():
        if not (th.worker is None):
            if not (th.quiet):
                logger.warn("Terminating task worker ...")
            th.worker.terminate()
            th.worker = None

    def terminate_scheduler():
        if not (th.scheduler is None):
            if not (th.quiet):
                logger.warn("Terminating task scheduler ...")
            th.scheduler.terminate()
            th.scheduler = None

    ###################################################
    #                     CONFIG                      #
    ###################################################

    # ORM_HOOK OVERRIDE
    def task_config(self):
        """Add celery config"""
        th.app.conf.update(**CELERY_DEFAULT_CONFIGS)
        self.__scheduler = lambda: None
        th.quiet = QUIET


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
