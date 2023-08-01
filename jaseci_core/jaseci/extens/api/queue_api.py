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
        Monitor Queues. Check the task if it's still
            pending, running or already have the result
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
        Forcely wait the queues until executed.

        :param task_id: the task need to wait for result
        :param timeout: force timeout on your current request
            to avoid hang up if there's too many task running currently
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
        Create a scheduled walker

        :param name: name of the actual queue for reference.
        :param schedule: can be interval or cron.
            Format: {"type": {% interval or cron %}, "conf": {% conf %}, "one_off": {% true if one time only; default false %} }
            Interval conf: {"every": {% integer %}, "period": {% days | hours | minutes | seconds | microseconds %}
            cron conf: {"minute": "*", "hour": "*", "day_of_week": "*", "day_of_month": "*", "month_of_year": "*"}
        :param body: your periodic_task kwargs (dict)
            mst: requestor's master or superadmin requested master - defaults to requestor
            wlk: target walker - defaults to init
            ctx: context to be used upon call - defaults to {}
            nd: target node - defaults to root
            snt: preferred sentinel - defaults to master's active sentinel
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        from jaseci.prim.super_master import SuperMaster

        if not isinstance(self, SuperMaster) or not body.get("mst"):
            body["mst"] = self.jid

        return (
            "Scheduled Walker created successfully!"
            if task.add_scheduled_queue(task.scheduled_walker, name, schedule, body)
            else "Django is required to support scheduled walker!"
        )

    @Interface.admin_api()
    def add_scheduled_sequence(self, name: str, schedule: dict, body: dict):
        """
        Create a scheduled sequence. More like call multiple api in order.

        :param name: name of the actual queue for reference.
        :param schedule: can be interval or cron.
            Format: {"type": {% interval or cron %}, "conf": {% conf %}, "one_off": {% true if one time only; default false %} }
            Interval conf: {"every": {% integer %}, "period": {% days | hours | minutes | seconds | microseconds %}
            cron conf: {"minute": "*", "hour": "*", "day_of_week": "*", "day_of_month": "*", "month_of_year": "*"}
        :param body: refer to jaseci/docs/docs/deployment/extension_services/task.md
            under schedule sequence argument structure
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        return (
            "Scheduled Sequence created successfully!"
            if task.add_scheduled_queue(task.scheduled_sequence, name, schedule, body)
            else "Django is required to support scheduled walker!"
        )

    @Interface.private_api()
    def get_scheduled_queues(
        self, limit: int = 10, offset: int = 0, asc: bool = False, search: str = None
    ):
        """
        Get all periodic_task

        :param limit: result limit
        :param offset: query offset
        :param asc: sorting
        :param search: search by name
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        return task.get_scheduled_queues(limit, offset, asc, search, self)

    @Interface.private_api()
    def delete_scheduled_queue(self, scheduled_queue_id: int):
        """
        Delete specific periodic_task

        :param scheduled_queue_id: the id of periodic task to delete
        """
        task = JsOrc.svc("task", TaskService)
        if not task.is_running():
            return "Task hook is not yet initialized!"

        result = task.delete_scheduled_queue(scheduled_queue_id, self)
        if result == None:
            return "Django is required to support scheduled walker!"
        return (
            "Successfully deleted!"
            if result
            else f"Scheduled Queue with id({scheduled_queue_id}) is not existing!"
        )
