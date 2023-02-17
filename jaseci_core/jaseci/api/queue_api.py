"""
Queue api functions as a mixin
"""
from jaseci.api.interface import Interface
from jaseci import JsOrc
from jaseci.svc.task_svc import TaskService


class QueueApi:
    """
    Queue APIs

    APIs used for celery configuration and monitoring
    """

    @Interface.private_api(allowed_methods=["get"])
    def walker_queue_check(self, task_id: str = ""):
        """
        Monitor Queues
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        if not task_id:
            return task.inspect_tasks()
        else:
            return task.get_by_task_id(task_id)

    @Interface.private_api(allowed_methods=["get"])
    def walker_queue_wait(self, task_id: str, timeout: int = 30):
        """
        Wait Queues
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        if not task_id:
            return "Task id is required!"
        else:
            return task.get_by_task_id(task_id, True, timeout)
