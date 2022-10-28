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
            if self.enabled and self.is_ready():
                self.state = Ss.STARTED
                self.run(hook)
                self.state = Ss.RUNNING
                self.post_run(hook)
        except Exception as e:
            if not (self.quiet):
                logger.error(
                    f"Skipping {self.__class__.__name__} due to initialization "
                    f"failure!\n{e.__class__.__name__}: {e}"
                )
            self.failed()

        return self

    def run(self, hook=None):
        raise Exception(f"{COMMON_ERROR} Please override run method!")

    def post_run(self, hook=None):
        pass

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
            logger.exception(f"Error loading settings for {self.__class__}")
            self.config = DEFAULT_CONFIG
            self.kube = None

    def build_config(self, hook) -> dict:
        return DEFAULT_CONFIG

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


class ApplicationContext:
    def __init__(self):
        self.services = {}
        self.background = {}
        self.context = {}

    ###################################################
    #                 SERVICE HANDLER                 #
    ###################################################

    def add_service_builder(self, name, svc):
        if self.services.get(name):
            raise Exception(f"{name} already exists!")

        self.services[name] = svc

    def build_service(self, name, background, *args, **kwargs):

        svc = self.services.get(name)

        if not svc:
            logger.error(f"Service {name} is not yet set!")
            return None

        svc = svc(*args, **kwargs)

        if background:
            self.background[name] = svc

        return svc

    def get_service(self, name, *args, **kwargs):
        svc = self.background.get(name)

        if not svc:
            return self.build_service(name, True, *args, **kwargs)

        return svc

    ###################################################
    #                 CONTEXT HANDLER                 #
    ###################################################

    def add_context(self, name, cls, *args, **kwargs):
        self.context[name] = {"class": cls, "args": args, "kwargs": kwargs}

    def build_context(self, ctx, *args, **kwargs):
        ctx = self.context[ctx]
        return ctx["class"](*args, *ctx["args"], **kwargs, **ctx["kwargs"])


class MetaProperties:
    def __init__(self, cls):
        self.cls = cls

        if not hasattr(cls, "_app"):
            setattr(cls, "_app", None)
            setattr(cls, "_enabled", True)
            setattr(cls, "_state", Ss.NOT_STARTED)
            setattr(cls, "_quiet", False)
            setattr(cls, "_services", {})
            setattr(cls, "_background", {})
            setattr(cls, "_hook", None)
            setattr(cls, "_hook_param", {})
            setattr(cls, "_master", None)
            setattr(cls, "_super_master", None)

    @property
    def app(self) -> ApplicationContext:
        return self.cls._app

    @app.setter
    def app(self, val: ApplicationContext):
        self.cls._app = val

    @property
    def state(self) -> Ss:
        return self.cls._state

    @state.setter
    def state(self, val: Ss):
        self.cls._state = val

    @property
    def enabled(self) -> Ss:
        return self.cls._enabled

    @enabled.setter
    def enabled(self, val: Ss):
        return self.cls._enabled

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
