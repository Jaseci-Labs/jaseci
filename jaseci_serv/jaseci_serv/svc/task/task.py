from jaseci.svc import TaskService as Ts
from jaseci_serv.jaseci_serv.settings import TASK_CONFIG


#################################################
#                 TASK APP ORM                  #
#################################################


class TaskService(Ts):
    def get_config(self, hook) -> dict:
        return hook.build_config("TASK_CONFIG", TASK_CONFIG)
