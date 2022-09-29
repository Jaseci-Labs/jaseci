from celery import Celery
from celery.backends.base import DisabledBackend

from jaseci.svc import CommonService, ServiceState as Ss
from jaseci.utils.utils import logger
from .common import (
    TASK_CONFIG,
    Queue,
    ScheduledSequence,
    ScheduledWalker,
    TaskProperties,
)


#################################################
#                   TASK APP                   #
#################################################


class TaskService(CommonService, TaskProperties):

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        TaskProperties.__init__(self, __class__)
        CommonService.__init__(self, __class__, hook)

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def build(self, hook=None):
        configs = self.get_config(hook)
        enabled = configs.pop("enabled", True)

        if enabled:
            self.quiet = configs.pop("quiet", False)
            self.app = Celery("celery")
            self.app.conf.update(**configs)

            # -------------------- TASKS -------------------- #

            self.queue = self.app.register_task(Queue())
            self.scheduled_walker = self.app.register_task(ScheduledWalker())
            self.scheduled_sequence = self.app.register_task(ScheduledSequence())

            # ------------------ INSPECTOR ------------------ #

            self.inspect = self.app.control.inspect()
            self.ping()

            self.state = Ss.RUNNING

            # ------------------ PROCESS ------------------- #

            self.spawn_daemon(
                worker=self.app.Worker(quiet=self.quiet).start,
                scheduler=self.app.Beat(quiet=self.quiet).run,
            )
        else:
            self.state = Ss.DISABLED

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
            ret["status"] = "SUCCESS"
            ret["result"] = task.get(disable_sync_subtasks=False)

        return ret

    def inspect_tasks(self):
        return {
            "scheduled": self.inspect.scheduled(),
            "active": self.inspect.active(),
            "reserved": self.inspect.reserved(),
        }

    def ping(self):  # will throw exception
        self.inspect.ping()
        self.app.AsyncResult("").result

    ###################################################
    #                     QUEUING                     #
    ###################################################

    def add_queue(self, wlk, nd, *args):
        return self.queue.delay(wlk.id.urn, nd.id.urn, args).task_id

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def reset(self, hook):
        self.terminate_daemon("worker", "scheduler")
        self.inspect = None
        super().reset(hook)

    def failed(self):
        super().failed()
        self.terminate_daemon("worker", "scheduler")

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def contraints(self, hook=None):
        if not (hook is None) and hook.redis.has_failed():
            if not (self.quiet):
                logger.error(
                    "Redis is not yet running reason "
                    "for skipping Celery initialization!"
                )
            self.state = Ss.FAILED
            return False
        return True

    def get_config(self, hook) -> dict:
        return hook.build_config("TASK_CONFIG", TASK_CONFIG)
