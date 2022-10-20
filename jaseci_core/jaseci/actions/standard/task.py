"""Built in actions for Jaseci"""
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def get_result(task_id, wait, meta):
    """
    Get task result by task_id
    """
    task = meta["h"].task

    if not task.is_running():
        raise Exception("Task hook is not yet initialized!")

    return task.get_by_task_id(task_id, wait)
