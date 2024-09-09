from celery import Celery
from celery.schedules import crontab
from celery.app.trace import build_tracer
from celery.app.control import Inspect
from celery.backends.base import DisabledBackend

from jaseci.jsorc.jsorc import JsOrc
from jaseci.jsorc.jsorc_utils import ManifestType
from .tasks import Queue, ScheduledWalker, ScheduledSequence

#################################################
#                   TASK APP                   #
#################################################


@JsOrc.service(name="task", config="TASK_CONFIG")
class TaskService(JsOrc.CommonService):
    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(
        self,
        config: dict,
        manifest: dict,
        manifest_type: ManifestType = ManifestType.DEDICATED,
        source: dict = {},
    ):
        self.inspect: Inspect = None
        self.queue: Queue = None
        self.scheduled_walker: ScheduledWalker = None
        self.scheduled_sequence: ScheduledSequence = None

        super().__init__(config, manifest, manifest_type, source)

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self):
        self.app = Celery("celery")
        self.app.conf.update(**self.config)

        # -------------------- TASKS -------------------- #
        (
            self.queue,
            self.scheduled_walker,
            self.scheduled_sequence,
        ) = self.register_tasks(Queue, ScheduledWalker, ScheduledSequence)

        # ------------------ INSPECTOR ------------------ #

        self.inspect = self.app.control.inspect()
        self.ping()

    def post_run(self):
        self.spawn_daemon(
            worker=self.app.Worker(quiet=self.quiet).start,
            scheduler=self.app.Beat(socket_timeout=None, quiet=self.quiet).run,
        )

    def register_tasks(self, *tasks) -> tuple:
        registered = []
        for task in tasks:
            task = self.app.register_task(task())
            task.__trace__ = build_tracer(task.name, task, app=self.app)
            registered.append(task)
        return tuple(registered)

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
        return self.queue.delay(wlk.jid, nd.jid, args).task_id

    ###################################################
    #                SCHEDULED QUEUING                #
    ###################################################

    def add_scheduled_queue(
        self, queue_type: object, name: str, schedule: dict, body: dict
    ):
        return None

    def get_scheduled_queues(
        self,
        limit: int = 10,
        offset: int = 0,
        asc: bool = True,
        name: str = None,
        master=False,
    ):
        return []

    def delete_scheduled_queue(self, scheduled_queue_id: int, master):
        return None

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def failed(self, error):
        super().failed(error)
        self.terminate_daemon("worker", "scheduler")

    # ---------------- PROXY EVENTS ----------------- #

    def on_delete(self):
        self.terminate_daemon("worker", "scheduler")

    ###################################################
    #                      UTILS                      #
    ###################################################

    def get_task_name(self, task):
        cls = type(task)
        module = cls.__module__
        name = cls.__qualname__
        if module is not None and module != "__builtin__":
            name = module + "." + name
        return name
