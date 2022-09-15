from jaseci.svc import task_svc as ts
from jaseci_serv.jaseci_serv.settings import TASK_CONFIG


#################################################
#                 TASK APP ORM                  #
#################################################


class task_svc(ts):
    def get_config(self, hook) -> dict:
        return hook.build_config("TASK_CONFIG", TASK_CONFIG)
