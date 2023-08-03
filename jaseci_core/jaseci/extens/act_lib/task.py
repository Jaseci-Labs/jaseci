"""Built in actions for Jaseci"""
from jaseci.jsorc.jsorc import JsOrc
from jaseci.jsorc.live_actions import jaseci_action
from jaseci.extens.svc.task_svc import TaskService


@jaseci_action()
def get_result(task_id, wait=False, timeout=30):
    """
    Get task result by task_id
    """

    return JsOrc.svc("task").poke(TaskService).get_by_task_id(task_id, wait, timeout)
