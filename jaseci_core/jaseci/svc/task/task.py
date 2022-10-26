from celery import Celery
from celery.app.control import Inspect
from celery.backends.base import DisabledBackend

from jaseci.svc import CommonService
from .common import Queue, ScheduledWalker, ScheduledSequence
from .config import TASK_CONFIG

#################################################
#                   TASK APP                   #
#################################################


class TaskService(CommonService):

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        self.inspect: Inspect = None
        self.queue: Queue = None
        self.scheduled_walker: ScheduledWalker = None
        self.scheduled_sequence: ScheduledSequence = None

        super().__init__(hook)

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.app = Celery("celery")
        self.app.conf.update(**self.config)

        # -------------------- TASKS -------------------- #

        self.queue = self.app.register_task(Queue())
        self.scheduled_walker = self.app.register_task(ScheduledWalker())
        self.scheduled_sequence = self.app.register_task(ScheduledSequence())

        # ------------------ INSPECTOR ------------------ #

        self.inspect = self.app.control.inspect()
        self.ping()

    def post_run(self, hook=None):
        self.spawn_daemon(
            worker=self.app.Worker(quiet=self.quiet).start,
            scheduler=self.app.Beat(socket_timeout=None, quiet=self.quiet).run,
        )

    ###################################################
    #              COMMON GETTER/SETTER               #
    ###################################################

    def get_by_task_id(self, task_id, wait=False, timeout=30):
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
            ret["result"] = task.get(timeout=timeout, disable_sync_subtasks=False)

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

    def build_config(self, hook) -> dict:
        return hook.service_glob("TASK_CONFIG", TASK_CONFIG)
