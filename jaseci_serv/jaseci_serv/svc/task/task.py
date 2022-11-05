from jaseci.svc import TaskService as Ts
from jaseci_serv.configs import TASK_CONFIG


#################################################
#                 TASK APP ORM                  #
#################################################


class TaskService(Ts):
    def build_config(self, hook) -> dict:
        return hook.service_glob("TASK_CONFIG", TASK_CONFIG)
