import signal
import sys
from multiprocessing import Process

from jaseci.utils.utils import logger
from .state import ServiceState as Ss


class CommonService:

    _daemon = {}

    def __init__(self, cls, hook=None):
        self.cls = cls
        if not hasattr(cls, "_app"):
            setattr(cls, "_app", None)
            setattr(cls, "_state", Ss.NOT_STARTED)
            setattr(cls, "_quiet", True)

        self.__build(hook)

    ###################################################
    #                   PROPERTIES                    #
    ###################################################

    # ------------------- DAEMON -------------------- #

    @property
    def daemon(self):
        return __class__._daemon

    # ----------------------------------------------- #

    @property
    def app(self):
        return self.cls._app

    @app.setter
    def app(self, val):
        self.cls._app = val

    @property
    def state(self) -> Ss:
        return self.cls._state

    @state.setter
    def state(self, val: Ss):
        self.cls._state = val

    @property
    def quiet(self) -> bool:
        return self.cls._quiet

    @quiet.setter
    def quiet(self, val: bool):
        self.cls._quiet = val

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def __build(self, hook=None):
        try:
            if self.is_ready() and self.contraints(hook):
                self.state = Ss.STARTED
                self.build(hook)
        except Exception as e:
            if not (self.quiet):
                logger.error(
                    f"Skipping {self.__class__.__name__} due to initialization failure!\n"
                    f"{e.__class__.__name__}: {e}"
                )
            self.failed()

    def build(self, hook=None):
        raise Exception("Not properly configured! Please override build method!")

    ###################################################
    #                     COMMONS                     #
    ###################################################

    def is_ready(self):
        return self.state.is_ready() and self.app is None

    def is_running(self):
        return self.state.is_running() and not (self.app is None)

    def has_failed(self):
        return self.state.has_failed()

    # ------------------- DAEMON -------------------- #

    def spawn_daemon(self, **targets):
        for name, target in targets.items():
            dae: Process = self.daemon.get(name)
            if not dae or not dae.is_alive():
                proc = Process(target=target)
                proc.daemon = True
                proc.start()
                self.daemon[name] = proc

    def terminate_daemon(self, *names):
        for name in names:
            dae: Process = self.daemon.pop(name, None)
            if not (dae is None) and dae.is_alive():
                logger.warn(f"Terminating {name} ...")
                dae.terminate()

    # --------------- TO BE OVERRIDEN --------------- #

    def contraints(self, hook=None):
        return True

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def reset(self, hook):
        self.app = None
        self.state = Ss.NOT_STARTED
        self.__init__(hook)

    def failed(self):
        self.app = None
        self.state = Ss.FAILED


class ProxyService(CommonService):
    def __init__(self):
        super().__init__(ProxyService)


class MetaProperties:
    def __init__(self, cls):
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
#                 PROCESS CLEANER                 #
###################################################


def force_terminate(*args):
    sys.exit(0)


signal.signal(signal.SIGINT, force_terminate)
