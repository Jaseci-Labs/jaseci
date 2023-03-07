"""Built in actions for Jaseci"""
from jaseci import JsOrc
from jaseci.actions.live_actions import jaseci_action
from jaseci.svc.task_svc import TaskService


@jaseci_action()
def get_result(task_id, wait, meta):
    """
    Get task result by task_id
    """

    return JsOrc.svc("task").poke(TaskService).get_by_task_id(task_id, wait)
