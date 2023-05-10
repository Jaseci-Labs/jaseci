import signal
import psycopg2

from time import sleep
from copy import deepcopy
from json import dumps
from datetime import datetime
from typing import TypeVar, Any, Union

from jaseci.utils.utils import logger
from jaseci.jsorc.jsorc_settings import JsOrcSettings
from jaseci.jsorc.jsorc_utils import State, CommonService as cs, ManifestType

from kubernetes.client.rest import ApiException

# For future use
# from concurrent.futures import ThreadPoolExecutor
# from os import cpu_count

T = TypeVar("T")


class JsOrc:
    # ------------------- ALIAS ------------------- #

    CommonService = cs

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

    _config = None
    _backoff_interval = 10
    _running_interval = 0
    __running__ = False
    __proxy__ = cs.proxy()

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
    def configure(cls):
        config: dict = cls.settings("JSORC_CONFIG")

        if cls.db_check():
            hook = cls.hook()
            config = hook.get_or_create_glob("JSORC_CONFIG", config)

        cls._config = config
        cls._backoff_interval = max(5, config.get("backoff_interval", 10))
        cls._regeneration_queues = config.get("pre_loaded_services", [])

    @classmethod
    def run(cls):
        if not cls.__running__:
            cls.__running__ == True
            cls.configure()
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
    def _svc(cls, service: str) -> cs:
        if service not in cls._services:
            raise Exception(f"Service {service} is not existing!")

        # highest priority
        instance = cls._services[service][0]

        config = cls.settings(instance["config"], cls.settings("DEFAULT_CONFIG"))
        manifest = cls.settings(
            instance["manifest"] or "DEFAULT_MANIFEST", cls.settings("DEFAULT_MANIFEST")
        )

        if cls.db_check():
            hook = cls.hook(use_proxy=instance["proxy"])

            config = hook.get_or_create_glob(instance["config"], config)

            manifest = (
                hook.get_or_create_glob(instance["manifest"], manifest)
                if instance["manifest"]
                else {}
            )

        instance: cs = instance["type"](
            config, manifest, instance["manifest_type"], instance
        )

        if instance.has_failed() and service not in cls._regeneration_queues:
            cls._regeneration_queues.append(service)

        return instance

    @classmethod
    def svc(cls, service: str, cast: T = None) -> Union[T, cs]:
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
    def svc_reset(cls, service, cast: T = None) -> Union[T, cs]:
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
        manifest_type: ManifestType = ManifestType.DEDICATED,
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
        manifest_type: manifest process type
        """

        def decorator(service: T) -> T:
            cls.push(
                name=name or service.__name__,
                target=cls._services,
                entry={
                    "type": service,
                    "config": config or f"{name.upper()}_CONFIG",
                    "manifest": manifest,
                    "manifest_type": manifest_type,
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

    @classmethod
    def overrided_namespace(
        cls, name: str, manifest_type: ManifestType = ManifestType.DEDICATED
    ) -> tuple:
        manual_namespace = cls.settings("SERVICE_MANIFEST_MAP").get(name)
        if manual_namespace:
            if manual_namespace == "SOURCE":
                manifest_type = ManifestType.SOURCE
            else:
                manual_namespace == manual_namespace.lower()
                manifest_type = ManifestType.MANUAL
                return manifest_type, manual_namespace

        return (manifest_type,)

    #################################################
    #                  AUTOMATION                   #
    #################################################

    @classmethod
    def add_regeneration_queue(cls, service: str):
        cls.svc(service).state = State.RESTART
        cls._regeneration_queues.append(service)

    @classmethod
    def regenerate(cls):
        if not cls._regenerating:
            cls._regenerating = True

            if cls._has_db:
                cls.regenerate_service()
            else:
                cls.regenerate_database()

            cls._regenerating = False

    @classmethod
    def regenerate_service(cls):
        from jaseci.extens.svc.kube_svc import KubeService
        from jaseci.utils.actions.actions_manager import ActionManager

        kube = cls.svc("kube", KubeService)
        regeneration_queues = cls._regeneration_queues.copy()
        cls._regeneration_queues.clear()
        while regeneration_queues:
            regeneration_queue = regeneration_queues.pop(0)
            service = cls.svc(regeneration_queue)
            hook = cls.hook(use_proxy=service.source["proxy"])
            if not service.is_running() and service.enabled and service.automated:
                if service.manifest and kube.is_running():
                    try:
                        manifest = kube.resolve_manifest(
                            hook.get_or_create_glob(
                                service.source["manifest"], service.manifest
                            ),
                            *cls.overrided_namespace(
                                regeneration_queue, service.manifest_type
                            ),
                        )

                        rmhists: dict = hook.get_or_create_glob(
                            "RESOLVED_MANIFEST_HISTORY", {}
                        )

                        _rmhist = rmhists.get(service.source["manifest"], [{}])[0]
                        rmhist = deepcopy(_rmhist)

                        for kind, confs in manifest.items():
                            for name, conf in confs.items():
                                namespace = conf["metadata"].get("namespace")

                                if kind in rmhist and name in rmhist[kind]:
                                    rmhist[kind].pop(name, None)

                                res = kube.read(kind, name, namespace)
                                if hasattr(res, "status") and res.status == 404:
                                    kube.create(kind, name, conf, namespace)
                                elif not isinstance(res, ApiException):
                                    config_version = 1

                                    if isinstance(res, dict):
                                        if "labels" in res["metadata"]:
                                            config_version = (
                                                res["metadata"]
                                                .get("labels", {})
                                                .get("config_version", 1)
                                            )
                                    elif res.metadata.labels:
                                        config_version = res.metadata.labels.get(
                                            "config_version", 1
                                        )

                                    if config_version != conf.get("metadata").get(
                                        "labels", {}
                                    ).get("config_version", 1):
                                        kube.patch(kind, name, conf, namespace)

                        for kind, confs in rmhist.items():
                            for name, conf in confs.items():
                                namespace = conf["metadata"].get("namespace")
                                res = kube.read(kind, name, namespace, quiet=True)
                                if not isinstance(res, ApiException) and (
                                    (isinstance(res, dict) and res.get("metadata"))
                                    or res.metadata
                                ):
                                    if kind not in cls.settings(
                                        "UNSAFE_KINDS"
                                    ) or service.manifest_unsafe_paraphrase == cls.settings(
                                        "UNSAFE_PARAPHRASE"
                                    ):
                                        kube.delete(kind, name, namespace)
                                    else:
                                        logger.info(
                                            f"You don't have permission to delete `{kind}` for `{name}` with namespace `{namespace}`!"
                                        )

                        if _rmhist != manifest:
                            if service.source["manifest"] not in rmhists:
                                rmhists[service.source["manifest"]] = [manifest]
                            else:
                                rmhists[service.source["manifest"]].insert(0, manifest)
                            hook.save_glob("RESOLVED_MANIFEST_HISTORY", dumps(rmhists))
                            hook.commit()

                    except Exception as e:
                        logger.error(f"Unhandled exception: {e}")

                cls.svc_reset(regeneration_queue)

        action_manager = cls.get("action_manager", ActionManager)
        action_manager.optimize(jsorc_interval=cls._backoff_interval)
        action_manager.record_system_state()

    @classmethod
    def regenerate_database(cls):
        from jaseci.extens.svc.kube_svc import KubeService

        kube = cls.svc("kube", KubeService)

        if kube.is_running():
            while not cls.db_check():
                for kind, confs in kube.resolve_manifest(
                    cls.settings("DB_REGEN_MANIFEST", {}),
                    *cls.overrided_namespace("database"),
                ).items():
                    for name, conf in confs.items():
                        namespace = conf["metadata"].get("namespace")
                        res = kube.read(kind, name, namespace)
                        if hasattr(res, "status") and res.status == 404 and conf:
                            kube.create(kind, name, conf, namespace)
                sleep(1)
        raise SystemExit("Force termination to restart the pod!")

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

    # wait interval_check to be finished before decrement
    JsOrc._running_interval -= 1
    JsOrc.push_interval(JsOrc._backoff_interval)


signal.signal(signal.SIGALRM, interval_check)
