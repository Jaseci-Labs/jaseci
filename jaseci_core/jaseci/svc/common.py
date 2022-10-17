import threading
from threading import Thread
from ctypes import c_long, py_object, pythonapi

from jaseci.utils.utils import logger
from .state import ServiceState as Ss

COMMON_ERROR = "Not properly configured!"
DEFAULT_CONFIG = {"enabled": False}


class CommonService:

    _daemon = {}

    def __init__(self, hook=None):
        self.app = None
        self.enabled = False
        self.state = Ss.NOT_STARTED
        self.quiet = True
        self.build_settings(hook)

    ###################################################
    #                   PROPERTIES                    #
    ###################################################

    # ------------------- DAEMON -------------------- #

    @property
    def daemon(self):
        return __class__._daemon

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def start(self, hook=None):
        try:
            if self.is_ready():
                self.state = Ss.STARTED
                self.run(hook)
        except Exception as e:
            if not (self.quiet):
                logger.error(
                    f"Skipping {self.__class__.__name__} due to initialization "
                    f"failure!\n{e.__class__.__name__}: {e}"
                )
            self.failed()

        return self

    def run(self, hook=None):
        raise Exception(f"{COMMON_ERROR} Please override build method!")

    ###################################################
    #                     COMMONS                     #
    ###################################################

    def is_ready(self):
        return self.state.is_ready() and self.app is None

    def is_running(self):
        return self.state.is_running() and not (self.app is None)

    def has_failed(self):
        return self.state.has_failed()

    def build_settings(self, hook) -> dict:
        try:
            self.kube = self.build_kube(hook)
            config = self.build_config(hook)
            self.enabled = config.pop("enabled", False)
            self.quiet = config.pop("quiet", False)
            self.config = config
        except Exception:
            self.config = DEFAULT_CONFIG
            self.kube = None

    def build_config(self, hook) -> dict:
        pass

    def build_kube(self, hook) -> dict:
        pass

    # ------------------- DAEMON -------------------- #

    def spawn_daemon(self, **targets):
        for name, target in targets.items():
            dae: ClosableThread = self.daemon.get(name)
            if not dae or not dae.is_alive():
                thread = ClosableThread(target=target, daemon=True)
                thread.start()
                self.daemon[name] = thread

    def terminate_daemon(self, *names):
        for name in names:
            dae: ClosableThread = self.daemon.pop(name, None)
            if not (dae is None) and dae.is_alive():
                logger.info(f"Terminating {name} ...")
                dae.force_close()

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def reset(self, hook):
        self.app = None
        self.state = Ss.NOT_STARTED
        self.__init__(hook)
        self.start(hook)

    def failed(self):
        self.app = None
        self.state = Ss.FAILED


class ProxyService(CommonService):
    def __init__(self):
        super().__init__(__class__)


class MetaProperties:
    def __init__(self, cls):
        self.cls = cls
        if not hasattr(cls, "_services"):
            setattr(cls, "_services", {})
            setattr(cls, "_background", {})
            setattr(cls, "_hook", None)
            setattr(cls, "_hook_param", {})
            setattr(cls, "_master", None)
            setattr(cls, "_super_master", None)

    @property
    def services(self) -> dict:
        return self.cls._services

    @services.setter
    def services(self, val: dict):
        self.cls._services = val

    @property
    def background(self) -> dict:
        return self.cls._background

    @background.setter
    def background(self, val: dict):
        self.cls._background = val

    @property
    def hook(self):
        return self.cls._hook

    @hook.setter
    def hook(self, val):
        self.cls._hook = val

    @property
    def hook_param(self) -> dict:
        return self.cls._hook_param

    @hook_param.setter
    def hook_param(self, val: dict):
        self.cls._hook_param = val

    @property
    def master(self):
        return self.cls._master

    @master.setter
    def master(self, val):
        self.cls._master = val

    @property
    def super_master(self):
        return self.cls._super_master

    @super_master.setter
    def super_master(self, val):
        self.cls._super_master = val


# ----------------------------------------------- #


###################################################
#                  CUSTOM THREAD                  #
###################################################


class ClosableThread(Thread):
    def force_close(self):
        if self.is_alive() and not hasattr(self, "_thread_id"):
            for tid, tobj in threading._active.items():
                if tobj is self:
                    self._thread_id = tid
                    break

            if (
                pythonapi.PyThreadState_SetAsyncExc(
                    c_long(self._thread_id), py_object(SystemExit)
                )
                != 1
            ):
                pythonapi.PyThreadState_SetAsyncExc(c_long(self._thread_id), None)
                raise SystemError("Failed to force close running thread!")

        self.join()
