from typing import overload, Literal, Union

from jaseci.svc.common_svc import common_svc
from jaseci.svc.redis.redis_svc import redis_svc
from jaseci.svc.task.task_svc import task_svc
from jaseci.svc.mail.mail_svc import mail_svc
from jaseci.svc.service_state import ServiceState as SS

from jaseci.utils.utils import logger


class meta_svc(common_svc):

    _services = {}

    # optional also mostly for custom service
    _background = {}

    def __init__(self):
        super().__init__(meta_svc)

        if self.is_ready():
            self.state = SS.RUNNING
            self.app = {
                "hook": self.build_hook,
                "master": self.build_master,
                "super_master": self.build_super_master,
            }

    ################################################
    #                ADDON SERVICE                 #
    ################################################

    # args & kwargs will be used as *args & **kwargs on initialization
    def add_service_builder(name, svc, custom=False, args=[], kwargs={}):
        if __class__._services.get(name):
            raise Exception(f"{name} already exists!")

        if not custom and not issubclass(svc, common_svc):
            raise Exception(f"{svc.__class__.__name__} is not instance of common_svc!")

        __class__._services[name] = {"class": svc, "args": args, "kwargs": kwargs}

    def run_service(name, background=False):
        svc = __class__._services.get(name, False)

        if not svc:
            logger.error(f"Service {name} is not yet set!")
            return

        svc = svc["class"](*svc["args"], **svc["kwargs"])

        if background:
            __class__._background[name] = svc

        return svc

    def get_service(name):
        svc = __class__._background.get(name, False)

        if not svc:
            logger.error(f"Service {name} is not running on background!")
            return

        return svc

    ################################################
    #                     HOOK                     #
    ################################################

    def hook(self):
        h = self.app["hook"]()
        h.redis = redis_svc(h)
        h.task = task_svc(h)
        h.mail = mail_svc(h)
        return h

    def build_hook(self):
        from jaseci.utils.redis_hook import redis_hook

        return redis_hook()

    ################################################
    #                   MASTERS                    #
    ################################################

    def __common(self, t, *args, **kwargs):
        if not kwargs.get("h", None):
            kwargs["h"] = self.hook()
        return self.app[t](*args, **kwargs)

    def master(self, *args, **kwargs):
        return self.__common("master", *args, **kwargs)

    def super_master(self, *args, **kwargs):
        return self.__common("super_master", *args, **kwargs)

    def build_master(self, *args, **kwargs):
        from jaseci.element.master import master

        return master(*args, **kwargs)

    def build_super_master(self, *args, **kwargs):
        from jaseci.element.super_master import super_master

        return super_master(*args, **kwargs)
