import signal
import psycopg2

from enum import Enum
from time import sleep
from copy import deepcopy
from datetime import datetime
from typing import TypeVar, Any, Union

from .utils.utils import logger
from .jsorc_settings import JsOrcSettings

from kubernetes.client.rest import ApiException
from multiprocessing import Process, current_process

# For future use
# from concurrent.futures import ThreadPoolExecutor
# from os import cpu_count

T = TypeVar("T")


class State(Enum):
    FAILED = -1
    NOT_STARTED = 0
    STARTED = 1
    RUNNING = 2

    def is_ready(self):
        return self == State.NOT_STARTED

    def is_running(self):
        return self == State.RUNNING

    def has_failed(self):
        return self == State.FAILED


class JsOrc:
    #######################################################################################################
    #                                             INNER CLASS                                             #
    #######################################################################################################

    class CommonService:
        ###################################################
        #                   PROPERTIES                    #
        ###################################################

        # ------------------- DAEMON -------------------- #

        _daemon = {}

        @property
        def daemon(self):
            return __class__._daemon

        def __init__(self, config: dict, manifest: dict):
            self.app = None
            self.error = None
            self.state = State.NOT_STARTED

            # ------------------- CONFIG -------------------- #

            self.config = config
            self.enabled = config.pop("enabled", False)
            self.quiet = config.pop("quiet", False)
            self.automated = config.pop("automated", False)

            # ------------------ MANIFEST ------------------- #

            self.manifest = manifest
            self.manifest_meta = {
                "__OLD_CONFIG__": manifest.pop("__OLD_CONFIG__", {}),
                "__UNSAFE_PARAPHRASE__": manifest.pop("__UNSAFE_PARAPHRASE__", ""),
            }

            self.start()

        ###################################################
        #                     BUILDER                     #
        ###################################################

        def start(self):
            try:
                if self.enabled and self.is_ready():
                    self.state = State.STARTED
                    self.run()
                    self.state = State.RUNNING
                    self.post_run()
            except Exception as e:
                if not (self.quiet):
                    logger.error(
                        f"Skipping {self.__class__.__name__} due to initialization "
                        f"failure!\n{e.__class__.__name__}: {e}"
                    )
                self.failed(e)

            return self

        def run(self):
            raise Exception(f"Not properly configured! Please override run method!")

        def post_run(self):
            pass

        # ------------------- DAEMON -------------------- #

        def spawn_daemon(self, **targets):
            if current_process().name == "MainProcess":
                for name, target in targets.items():
                    dae: Process = self.daemon.get(name)
                    if not dae or not dae.is_alive():
                        process = Process(target=target, daemon=True)
                        process.start()
                        self.daemon[name] = process

        def terminate_daemon(self, *names):
            for name in names:
                dae: Process = self.daemon.pop(name, None)
                if not (dae is None) and dae.is_alive():
                    logger.info(f"Terminating {name} ...")
                    dae.terminate()

        ###################################################
        #                     COMMONS                     #
        ###################################################

        def poke(self, cast: T = None, msg: str = None) -> Union[T, Any]:
            if self.is_running():
                return (
                    self
                    if cast and cast.__name__ == self.__class__.__name__
                    else self.app
                )
            raise Exception(
                msg or f"{self.__class__.__name__} is disabled or not yet configured!"
            )

        def is_ready(self):
            return self.state.is_ready() and self.app is None

        def is_running(self):
            return self.state.is_running() and not (self.app is None)

        def has_failed(self):
            return self.state.has_failed()

        def failed(self, error: Exception = None):
            self.app = None
            self.state = State.FAILED
            self.error = error

        @classmethod
        def proxy(cls):
            return cls({}, {})

        # ---------------- PROXY EVENTS ----------------- #

        def on_delete(self):
            pass

        # ------------------- EVENTS -------------------- #

        def __del__(self):
            self.on_delete()

        def __getstate__(self):
            return {}

        def __setstate__(self, ignored):
            # for build on pickle load
            self.state = State.FAILED
            del self

    #######################################################################################################
    #                                             JSORC CLASS                                             #
    #######################################################################################################

    # ----------------- REFERENCE ----------------- #

    _contexts = {}
    _context_instances = {}

    _services = {}
    _service_instances = {}

    _repositories = {}

    # ----------------- SETTINGS ----------------- #

    _use_proxy = False
    _settings = JsOrcSettings

    # For future use
    # _executor = ThreadPoolExecutor(
    #     min(4, int((cpu_count() or 2) / 4) + 1)
    # )

    # ------------------ COMMONS ------------------ #

    _backoff_interval = 10
    _running_interval = 0
    __running__ = False
    __proxy__ = CommonService.proxy()

    # ------------------- REGEN ------------------- #

    _regeneration_queues = []
    _regenerating = False
    _has_db = False

    @staticmethod
    def push(name: str, target: dict, entry: dict):
        if name not in target:
            target[name] = [entry]
        else:
            target[name] = sorted(
                target[name] + [entry],
                key=lambda item: (-item["priority"], -item["date_added"]),
            )

    @classmethod
    def run(cls):
        if not cls.__running__:
            cls.__running__ == True
            hook = cls.hook()
            config = hook.service_glob("JSORC_CONFIG", cls.settings("JSORC_CONFIG"))
            cls._backoff_interval = max(5, config.get("backoff_interval", 10))
            cls._regeneration_queues = config.get("pre_loaded_services", [])
            cls.push_interval(1)

    @classmethod
    def push_interval(cls, interval):
        if cls._running_interval == 0:
            cls._running_interval += 1
            signal.alarm(interval)
        else:
            logger.info("Reusing current running interval...")

    @classmethod
    def kube(cls):
        if not cls._kube:
            raise Exception(f"Kubernetes is not yet ready!")
        return cls._kube

    #################################################
    #                    HELPER                     #
    #################################################

    # ------------------ context ------------------ #

    @classmethod
    def get(cls, context: str, cast: T = None, *args, **kwargs) -> Union[T, Any]:
        """
        Get existing context instance or build a new one that will persists
        ex: master

        context: name of the context to be build
        cast: to cast the return and allow code hinting
        *arsgs: additional argument used to initialize context
        **kwargs: additional keyword argument used to initialize context
        """
        if context not in cls._contexts:
            raise Exception(f"Context {context} is not existing!")

        if context not in cls._context_instances:
            cls._context_instances[context] = cls.ctx(context, cast, *args, **kwargs)

        return cls._context_instances[context]

    @classmethod
    def destroy(cls, context: str):
        """
        remove existing context instance
        ex: master

        context: name of the context to be build
        """
        if context not in cls._contexts:
            raise Exception(f"Context {context} is not existing!")

        if context in cls._context_instances:
            del cls._context_instances[context]

    @classmethod
    def renew(cls, context: str, cast: T = None, *args, **kwargs) -> Union[T, Any]:
        """
        renew existing context instance or build a new one that will persists
        ex: master

        context: name of the context to be build
        cast: to cast the return and allow code hinting
        *arsgs: additional argument used to initialize context
        **kwargs: additional keyword argument used to initialize context
        """
        cls.destroy(context)

        cls._context_instances[context] = cls.ctx(context, cast, *args, **kwargs)
        return cls._context_instances[context]

    @classmethod
    def ctx(cls, context: str, cast: T = None, *args, **kwargs) -> Union[T, Any]:
        """
        Build new instance of the context
        ex: master

        context: name of the context to be build
        cast: to cast the return and allow code hinting
        *arsgs: additional argument used to initialize context
        **kwargs: additional keyword argument used to initialize context
        """
        if context not in cls._contexts:
            raise Exception(f"Context {context} is not existing!")

        # highest priority
        context = cls._contexts[context][0]

        return context["type"](*args, **kwargs)

    @classmethod
    def ctx_cls(cls, context: str):
        """
        Get the context class
        """
        if context not in cls._contexts:
            return None

        return cls._contexts[context][0]["type"]

    @classmethod
    def master(cls, cast: T = None, *args, **kwargs) -> Union[T, Any]:
        """
        Generate master instance
        """
        return cls.__gen_with_hook("master", cast, *args, **kwargs)

    @classmethod
    def super_master(cls, cast: T = None, *args, **kwargs) -> Union[T, Any]:
        """
        Generate super_master instance
        """
        return cls.__gen_with_hook("super_master", cast, *args, **kwargs)

    @classmethod
    def __gen_with_hook(cls, context: str, *args, **kwargs):
        """
        Common process on master and super_master
        """
        if not kwargs.get("h", None):
            kwargs["h"] = cls.hook()

        return cls.ctx(context, None, *args, **kwargs)

    # ------------------ service ------------------ #

    @classmethod
    def _svc(cls, service: str) -> CommonService:
        if service not in cls._services:
            raise Exception(f"Service {service} is not existing!")

        # highest priority
        instance = cls._services[service][0]

        hook = cls.hook(use_proxy=instance["proxy"])

        config = hook.service_glob(
            instance["config"],
            cls.settings(instance["config"], cls.settings("DEFAULT_CONFIG")),
        )

        manifest = (
            hook.service_glob(
                instance["manifest"],
                cls.settings(instance["manifest"], cls.settings("DEFAULT_MANIFEST")),
            )
            if instance["manifest"]
            else {}
        )

        instance: JsOrc.CommonService = instance["type"](config, manifest)

        if instance.has_failed() and service not in cls._regeneration_queues:
            cls._regeneration_queues.append(service)

        return instance

    @classmethod
    def svc(cls, service: str, cast: T = None) -> Union[T, CommonService]:
        """
        Get service. Initialize when not yet existing.
        ex: task

        service: name of the service to be reference
        cast: to cast the return and allow code hinting
        """
        if service not in cls._services:
            raise Exception(f"Service {service} is not existing!")

        if service not in cls._service_instances:
            if cls._use_proxy and cls._services[service][0]["proxy"]:
                return cls.__proxy__
            cls._service_instances[service] = cls._svc(service)

        return cls._service_instances[service]

    @classmethod
    def svc_reset(cls, service, cast: T = None) -> Union[T, CommonService]:
        """
        Service reset now deletes the actual instance and rebuild it
        """
        if service in cls._service_instances:
            instance = cls._service_instances.pop(service)
            del instance
        return cls.svc(service)

    # ---------------- repository ----------------- #

    @classmethod
    def src(cls, repository: str, cast: T = None) -> Union[T, Any]:
        """
        Initialize datasource class (repository)
        ex: hook

        repository: name of the repository to be reference
        cast: to cast the return and allow code hinting
        """
        if repository not in cls._repositories:
            raise Exception(f"Repository {repository} is not existing!")

        # highest priority
        repository = cls._repositories[repository][0]

        return repository["type"]()

    @classmethod
    def hook(cls, cast: T = None, use_proxy: bool = False) -> Union[T, Any]:
        """
        Generate hook repository instance
        """
        cls._use_proxy = use_proxy
        hook = cls.src("hook")
        cls._use_proxy = False
        return hook

    #################################################
    #                  DECORATORS                   #
    #################################################

    @classmethod
    def service(
        cls,
        name: str = None,
        config: str = None,
        manifest: str = None,
        priority: int = 0,
        proxy: bool = False,
    ):
        """
        Save the class in services options
        name: name to be used for reference
        config: config name from datasource
        manifest: manifest name from datasource
        priority: duplicate name will use the highest priority
        proxy: allow proxy service
        """

        def decorator(service: T) -> T:
            cls.push(
                name=name or service.__name__,
                target=cls._services,
                entry={
                    "type": service,
                    "config": config or f"{name.upper()}_CONFIG",
                    "manifest": manifest,
                    "priority": priority,
                    "proxy": proxy,
                    "date_added": int(datetime.utcnow().timestamp() * 1000),
                },
            )
            return service

        return decorator

    @classmethod
    def repository(cls, name: str = None, priority: int = 0):
        """
        Save the class in repositories options
        name: name to be used for reference
        priority: duplicate name will use the highest priority
        """

        def decorator(repository: T) -> T:
            cls.push(
                name=name or repository.__name__,
                target=cls._repositories,
                entry={
                    "type": repository,
                    "priority": priority,
                    "date_added": int(datetime.utcnow().timestamp() * 1000),
                },
            )
            return repository

        return decorator

    @classmethod
    def context(cls, name: str = None, priority: int = 0):
        """
        Save the class in contexts options
        name: name to be used for reference
        priority: duplicate name will use the highest priority
        """

        def decorator(context: T) -> T:
            cls.push(
                name=name or context.__name__,
                target=cls._contexts,
                entry={
                    "type": context,
                    "priority": priority,
                    "date_added": int(datetime.utcnow().timestamp() * 1000),
                },
            )
            return context

        return decorator

    @classmethod
    def inject(cls, contexts: list = [], services: list = [], repositories: list = []):
        """
        Allow to inject instance on specific method/class
        contexts: list of context name to inject
            - can use tuple per entry (name, alias) instead of string
        services: list of service name to inject
            - can use tuple per entry (name, alias) instead of string
        repositories: list of service name to inject
            - can use tuple per entry (name, alias) instead of string
        """

        def decorator(callable):
            def argument_handler(*args, **kwargs):
                _instances = {}

                for context in contexts:
                    if isinstance(context, tuple):
                        _instances[context[1]] = cls.ctx(context[0])
                    else:
                        _instances[context] = cls.ctx(context)
                for repository in repositories:
                    if isinstance(repository, tuple):
                        _instances[repository[1]] = cls.src(repository[0])
                    else:
                        _instances[repository] = cls.src(repository)
                for service in services:
                    if isinstance(service, tuple):
                        _instances[service[1]] = cls.svc(service[0])
                    else:
                        _instances[service] = cls.svc(service)

                kwargs.update(_instances)
                callable(*args, **kwargs)

            return argument_handler

        return decorator

    @classmethod
    def settings(cls, name: str, default: T = None) -> Union[T, Any]:
        return getattr(cls._settings, name, default)

    #################################################
    #                  AUTOMATION                   #
    #################################################

    @classmethod
    def regenerate(cls):
        if not cls._regenerating:
            cls._regenerating = True
            from jaseci.svc.kube_svc import KubeService

            if cls.db_check():
                from jaseci.utils.actions.actions_manager import ActionManager

                while cls._regeneration_queues:
                    regeneration_queue = cls._regeneration_queues.pop(0)
                    service = cls.svc(regeneration_queue)
                    kube = cls.svc("kube", KubeService)

                    if (
                        not service.is_running()
                        and service.enabled
                        and service.automated
                    ):
                        if service.manifest and kube.is_running():
                            pod_name = ""
                            old_config_map = deepcopy(
                                service.manifest_meta.get("__OLD_CONFIG__", {})
                            )
                            unsafe_paraphrase = service.manifest_meta.get(
                                "__UNSAFE_PARAPHRASE__", ""
                            )
                            for kind, confs in service.manifest.items():
                                for conf in confs:
                                    name = conf["metadata"]["name"]
                                    _confs = old_config_map.get(kind, {})
                                    if name in _confs.keys():
                                        _confs.pop(name)

                                    if kind == "Service":
                                        pod_name = name
                                    res = kube.read(
                                        kind,
                                        name,
                                        namespace=kube.resolve_namespace(conf),
                                    )
                                    if (
                                        hasattr(res, "status")
                                        and res.status == 404
                                        and conf
                                    ):
                                        kube.create(kind, name, conf)
                                    elif (
                                        not isinstance(res, ApiException)
                                        and res.metadata
                                    ):
                                        if res.metadata.labels:
                                            config_version = res.metadata.labels.get(
                                                "config_version", 1
                                            )
                                        else:
                                            config_version = 1

                                        if config_version != conf.get("metadata").get(
                                            "labels", {}
                                        ).get("config_version", 1):
                                            kube.patch(kind, name, conf)

                                if (
                                    old_config_map
                                    and type(old_config_map) is dict
                                    and kind in old_config_map
                                    and name in old_config_map[kind].keys()
                                ):
                                    old_config_map.get(kind, {}).pop(name)

                                for to_be_removed in old_config_map.get(
                                    kind, {}
                                ).keys():
                                    res = kube.read(
                                        kind,
                                        to_be_removed,
                                        namespace=kube.resolve_namespace(
                                            old_config_map["kind"][to_be_removed]
                                        ),
                                    )
                                    if (
                                        not isinstance(res, ApiException)
                                        and res.metadata
                                    ):
                                        if kind not in cls.settings(
                                            "UNSAFE_KINDS"
                                        ) or unsafe_paraphrase == cls.settings(
                                            "UNSAFE_PARAPHRASE"
                                        ):
                                            kube.delete(kind, to_be_removed)
                                        else:
                                            logger.info(
                                                f"You don't have permission to delete `{kind}` for `{to_be_removed}` with namespace `{kube.namespace}`!"
                                            )

                            if kube.is_pod_running(pod_name):
                                logger.info(
                                    f"Pod state is running. Trying to Restart {regeneration_queue}..."
                                )
                                cls.svc_reset(regeneration_queue)
                            else:
                                cls._regeneration_queues.append(regeneration_queue)
                        else:
                            cls.svc_reset(regeneration_queue)
                    sleep(1)

                action_manager = cls.get("action_manager", ActionManager)
                action_manager.optimize(jsorc_interval=cls._backoff_interval)
                action_manager.record_system_state()
            else:
                kube = cls.svc("kube", KubeService)
                for kind, confs in cls.settings("DB_REGEN_MANIFEST", {}).items():
                    for conf in confs:
                        name = conf["metadata"]["name"]
                        res = kube.read(kind, name)
                        if hasattr(res, "status") and res.status == 404 and conf:
                            kube.create(kind, name, conf)

                if cls.db_check():
                    dbrc = cls.settings("DB_REGEN_CONFIG")
                    kube.terminate_jaseci(dbrc["pod"])

            cls._regenerating = False

    @classmethod
    def db_check(cls):
        if not cls._has_db:
            try:
                dbrc = cls.settings("DB_REGEN_CONFIG")
                if dbrc["enabled"]:
                    connection = psycopg2.connect(
                        host=dbrc["host"],
                        dbname=dbrc["db"],
                        user=dbrc["user"],
                        password=dbrc["password"],
                        port=dbrc["port"],
                    )
                    connection.close()
                cls._has_db = True
            except Exception:
                cls._has_db = False
        return cls._has_db


def interval_check(signum, frame):
    JsOrc.regenerate()
    logger.info(
        f"Backing off for {JsOrc._backoff_interval} seconds before the next interval check..."
    )

    # wait interval_check to be finished before decrement
    JsOrc._running_interval -= 1
    JsOrc.push_interval(JsOrc._backoff_interval)


signal.signal(signal.SIGALRM, interval_check)
