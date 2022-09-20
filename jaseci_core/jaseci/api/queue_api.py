"""
Queue api functions as a mixin
"""
from jaseci.api.interface import Interface


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
        if not self._h.task.is_running():
            return "Task hook is not yet initialized!"

        if not task_id:
            return self._h.task.inspect_tasks()
        else:
            return self._h.task.get_by_task_id(task_id)

    @Interface.private_api(allowed_methods=["get"])
    def walker_queue_wait(self, task_id: str):
        """
        Wait Queues
        """
        if not self._h.task.is_running():
            return "Task hook is not yet initialized!"

        if not task_id:
            return "Task id is required!"
        else:
            return self._h.task.get_by_task_id(task_id, True)
