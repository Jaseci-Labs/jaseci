from jaseci_serv.jaseci_serv.settings import TASK_CONFIG
from jaseci.svc.task.task_svc import task_svc as ts


#################################################
#                 TASK APP ORM                  #
#################################################


class task_svc(ts):
    def get_config(self, hook) -> dict:
        return hook.build_config("TASK_CONFIG", TASK_CONFIG)
