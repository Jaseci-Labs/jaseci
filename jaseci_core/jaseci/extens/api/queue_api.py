"""
Queue api functions as a mixin
"""
from jaseci.extens.api.interface import Interface
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.task_svc import TaskService


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

    @Interface.private_api()
    def add_scheduled_walker(self, name: str, schedule: dict, body: dict = {}):
        """
        temp
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        from jaseci.prim.super_master import SuperMaster

        if not isinstance(self, SuperMaster) or not body.get("mst"):
            body["mst"] = self.jid

        return (
            "Schedued Walker created successfully!"
            if task.add_scheduled_queue(task.scheduled_walker, name, schedule, body)
            else "Django is required to support scheduled walker!"
        )

    @Interface.admin_api()
    def add_scheduled_sequence(self, name: str, schedule: dict, body: dict):
        """
        temp
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        return (
            "Schedued Sequence created successfully!"
            if task.add_scheduled_queue(task.scheduled_sequence, name, schedule, body)
            else "Django is required to support scheduled walker!"
        )

    @Interface.private_api()
    def get_scheduled_queues(
        self, limit: int = 10, offset: int = 0, asc: bool = False, search: str = None
    ):
        """
        temp
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        return task.get_scheduled_queues(limit, offset, asc, search, self)

    @Interface.private_api()
    def delete_scheduled_queue(self, scheduled_queue_id: int):
        """
        temp
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        result = task.delete_scheduled_queue(scheduled_queue_id, self)
        if result == None:
            return "Django is required to support scheduled walker!"
        return (
            "Successfully deleted"
            if result
            else f"Scheduled Queue with id({scheduled_queue_id}) is not existing!"
        )
