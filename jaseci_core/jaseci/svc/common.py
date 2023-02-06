from copy import deepcopy
from multiprocessing import Process

from kubernetes import config as kubernetes_config
from kubernetes.client import ApiClient, CoreV1Api, AppsV1Api, RbacAuthorizationV1Api
from kubernetes.client.rest import ApiException

from jaseci.utils.utils import logger
from jaseci.actions.live_actions import load_action_config
from jaseci.svc.actions_optimizer.actions_optimizer import ActionsOptimizer
from .state import ServiceState as Ss
from .config import META_CONFIG, KUBERNETES_CONFIG, DATABASE, POSTGRES_MANIFEST

import time
import numpy as np

import psycopg2

###################################################
#                  UNSAFE PARAMS                  #
###################################################

UNSAFE_PARAPHRASE = "I know what I'm doing!"
UNSAFE_KINDS = ["PersistentVolumeClaim"]

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

    def poke(self, msg: str = None):
        if self.is_running():
            return self.app
        raise Exception(
            msg or f"{self.__class__.__name__} is disabled or not yet configured!"
        )

    def is_ready(self):
        return self.state.is_ready() and self.app is None

    def is_running(self):
        return self.state.is_running() and not (self.app is None)

    def has_failed(self):
        return self.state.has_failed()

    def build_settings(self, hook) -> dict:
        try:
            self.manifest = self.build_manifest(hook)
            self.manifest_meta = {}
            if self.manifest:
                self.manifest_meta["__OLD_CONFIG__"] = self.manifest.pop(
                    "__OLD_CONFIG__", {}
                )
                self.manifest_meta["__UNSAFE_PARAPHRASE__"] = self.manifest.pop(
                    "__UNSAFE_PARAPHRASE__", ""
                )

            config = self.build_config(hook)
            self.enabled = config.pop("enabled", False)
            self.quiet = config.pop("quiet", False)
            self.config = config
        except Exception:
            logger.exception(f"Error loading settings for {self.__class__}")
            self.config = DEFAULT_CONFIG
            self.manifest = None
            self.manifest_meta = {}

    def build_config(self, hook) -> dict:
        return DEFAULT_CONFIG

    def build_manifest(self, hook) -> dict:
        pass

    # ------------------- DAEMON -------------------- #

    def spawn_daemon(self, **targets):
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
    #                     CLEANER                     #
    ###################################################

    def reset(self, hook, start=True):
        self.app = None
        self.state = Ss.NOT_STARTED
        self.__init__(hook)

        if start:
            self.start(hook)

    def failed(self):
        self.app = None
        self.state = Ss.FAILED


class ProxyService(CommonService):
    def __init__(self):
        super().__init__(__class__)


class Kube:
    def __init__(self, in_cluster: bool, config: dict):
        if in_cluster:
            kubernetes_config.load_incluster_config()
        else:
            kubernetes_config.load_kube_config()

        self.client = ApiClient(config)
        self.core = CoreV1Api(config)
        self.api = AppsV1Api(self.client)
        self.auth = RbacAuthorizationV1Api(self.client)
        self.ping()
        self.defaults()

    def ping(self):
        res = self.client.call_api("/readyz", "GET")
        return res[1] == 200

    def create(self, api, namespace, conf):
        if api.startswith("ClusterRole"):
            self.create_apis[api](body=conf)
        else:
            self.create_apis[api](namespace=namespace, body=conf)

    def patch(self, api, name, namespace, conf):
        if api.startswith("ClusterRole"):
            self.patch_apis[api](name=name, body=conf)
        else:
            self.patch_apis[api](name=name, namespace=namespace, body=conf)

    def read(self, api: str, name: str, namespace: str = None):
        if api.startswith("ClusterRole"):
            return self.read_apis[api](name=name)
        else:
            return self.read_apis[api](name=name, namespace=namespace)

    def delete(self, api: str, name: str, namespace: str = None):
        if api.startswith("ClusterRole"):
            return self.delete_apis[api](name=name)
        else:
            return self.delete_apis[api](name=name, namespace=namespace)

    def is_running(self, name: str, namespace: str):
        try:
            return (
                self.core.list_namespaced_pod(
                    namespace=namespace, label_selector=f"pod={name}"
                )
                .items[0]
                .status.phase
                == "Running"
            )
        except Exception:
            return False

    def defaults(self):
        self.create_apis = {
            "Service": self.core.create_namespaced_service,
            "Deployment": self.api.create_namespaced_deployment,
            "ConfigMap": self.core.create_namespaced_config_map,
            "ServiceAccount": self.core.create_namespaced_service_account,
            "ClusterRole": self.auth.create_cluster_role,
            "ClusterRoleBinding": self.auth.create_cluster_role_binding,
            "Secret": self.core.create_namespaced_secret,
            "PersistentVolumeClaim": (
                self.core.create_namespaced_persistent_volume_claim
            ),
            "DaemonSet": self.api.create_namespaced_daemon_set,
        }
        self.patch_apis = {
            "Service": self.core.patch_namespaced_service,
            "Deployment": self.api.patch_namespaced_deployment,
            "ConfigMap": self.core.patch_namespaced_config_map,
            "ServiceAccount": self.core.patch_namespaced_service_account,
            "ClusterRole": self.auth.patch_cluster_role,
            "ClusterRoleBinding": self.auth.patch_cluster_role_binding,
            "Secret": self.core.patch_namespaced_secret,
            "PersistentVolumeClaim": (
                self.core.patch_namespaced_persistent_volume_claim
            ),
            "DaemonSet": self.api.patch_namespaced_daemon_set,
        }
        self.delete_apis = {
            "Service": self.core.delete_namespaced_service,
            "Deployment": self.api.delete_namespaced_deployment,
            "ConfigMap": self.core.delete_namespaced_config_map,
            "ServiceAccount": self.core.delete_namespaced_service_account,
            "ClusterRole": self.auth.delete_cluster_role,
            "ClusterRoleBinding": self.auth.delete_cluster_role_binding,
            "Secret": self.core.delete_namespaced_secret,
            "PersistentVolumeClaim": (
                self.core.delete_namespaced_persistent_volume_claim
            ),
            "DaemonSet": self.api.delete_namespaced_daemon_set,
        }
        self.read_apis = {
            "Service": self.core.read_namespaced_service,
            "Endpoints": self.core.read_namespaced_endpoints,
            "Deployment": self.api.read_namespaced_deployment,
            "ConfigMap": self.core.read_namespaced_config_map,
            "ServiceAccount": self.core.read_namespaced_service_account,
            "ClusterRole": self.auth.read_cluster_role,
            "ClusterRoleBinding": self.auth.read_cluster_role_binding,
            "Secret": self.core.read_namespaced_secret,
            "PersistentVolumeClaim": self.core.read_namespaced_persistent_volume_claim,
            "DaemonSet": self.api.read_namespaced_daemon_set,
        }


class JsOrc:
    def __init__(self, meta):
        self.automated = False
        self.meta = meta
        self.services = {}
        self.background = {}
        self.context = {}
        self.benchmark = {
            "jsorc": {"active": False, "requests": {}},
            "actions_optimizer": {"active": False, "requests": {}},
        }
        self.actions_history = {"active": False, "history": []}
        self.actions_calls = {}
        self.system_states = {"active": False, "states": []}
        self.actions_optimizer = ActionsOptimizer(
            benchmark=self.benchmark["actions_optimizer"],
            actions_history=self.actions_history,
            actions_calls=self.actions_calls,
        )
        self.db_check()

    def db_check(self):
        try:
            if DATABASE["enabled"]:
                connection = psycopg2.connect(
                    host=DATABASE["host"],
                    dbname=DATABASE["db"],
                    user=DATABASE["user"],
                    password=DATABASE["password"],
                    port=DATABASE["port"],
                )
                connection.close()
            self.has_db = True
        except Exception:
            self.has_db = False

    def db_regen(self):
        for kind, confs in POSTGRES_MANIFEST.items():
            for conf in confs:
                name = conf["metadata"]["name"]
                res = self.read(kind, name, self.namespace)
                if hasattr(res, "status") and res.status == 404 and conf:
                    self.create(kind, name, self.namespace, conf)

        self.db_check()
        if self.has_db:
            for item in self.kubernetes.core.list_namespaced_pod(
                namespace=self.namespace, label_selector=f"pod={DATABASE['pod']}"
            ).items:
                self.kubernetes.core.delete_namespaced_pod(item["name"], self.namespace)

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def build(self):
        try:
            config = META_CONFIG
            if self.has_db:
                hook = self.build_context("hook")
                config = hook.service_glob("META_CONFIG", META_CONFIG)
                self.prometheus = self.meta.get_service("promon", hook)

            if config.pop("automation", False):
                self.kubernetes = Kube(**config.pop("kubernetes", KUBERNETES_CONFIG))
                self.actions_optimizer.kube = self.kubernetes
                self.backoff_interval = config.pop("backoff_interval", 10)
                self.namespace = config.pop("namespace", "default")
                self.actions_optimizer.namespace = self.namespace
                self.keep_alive = config.pop(
                    "keep_alive", ["promon", "redis", "task", "mail"]
                )
                self.automated = True
            else:
                self.automated = False
        except Exception:
            self.automated = False

    def interval_check(self):
        if self.has_db:
            hook = self.meta.build_hook()
            for svc in self.keep_alive:
                try:
                    self.check(self.namespace, svc, hook)
                except Exception as e:
                    logger.exception(
                        f"Error checking {svc} !\n" f"{e.__class__.__name__}: {e}"
                    )
            self.optimize(jsorc_interval=self.backoff_interval)
            self.record_system_state()
        else:
            self.db_regen()

    ###################################################
    #                   KUBERNETES                    #
    ###################################################

    def in_cluster(self):
        """
        Check if JSORC/Jaseci is running in a kubernetes cluster
        """
        try:
            if not hasattr(self, "kubernetes"):
                return False
            return self.kubernetes.ping()
        except ApiException as e:
            logger.info(f"Kubernetes cluster environment check failed: {e}")
            return False

    def create(self, kind: str, name: str, namespace: str, conf: dict):
        try:
            logger.info(f"Creating {kind} for `{name}` with namespace `{namespace}`")
            self.kubernetes.create(kind, namespace, conf)
        except ApiException as e:
            logger.error(
                f"Error creating {kind} for `{name}` with namespace `{namespace}` -- {e}"
            )

    def patch(self, kind: str, name: str, namespace: str, conf: dict):
        try:
            logger.info(f"Patching {kind} for `{name}` with namespace `{namespace}`")
            self.kubernetes.patch(kind, name, namespace, conf)
        except ApiException as e:
            logger.error(
                f"Error patching {kind} for `{name}` with namespace `{namespace}` -- {e}"
            )

    def read(self, kind: str, name: str, namespace: str):
        try:
            logger.info(f"Retrieving {kind} for `{name}` with namespace `{namespace}`")
            return self.kubernetes.read(kind, name, namespace=namespace)
        except ApiException as e:
            logger.error(
                f"Error retrieving {kind} for `{name}` with namespace `{namespace}` -- {e}"
            )
            return e

    def delete(self, kind: str, name: str, namespace: str):
        try:
            logger.info(f"Deleting {kind} for `{name}` with namespace `{namespace}`")
            return self.kubernetes.delete(kind, name, namespace=namespace)
        except ApiException as e:
            logger.error(
                f"Error deleting {kind} for `{name}` with namespace `{namespace}` -- {e}"
            )
            return e

    def check(self, namespace, svc_name, hook):
        svc = self.meta.get_service(svc_name, hook)

        if not svc.is_running():
            if svc.manifest:
                config_map = svc.manifest
                pod_name = ""
                old_config_map = deepcopy(svc.manifest_meta.get("__OLD_CONFIG__", {}))
                unsafe_paraphrase = svc.manifest_meta.get("__UNSAFE_PARAPHRASE__", "")
                for kind, confs in config_map.items():
                    for conf in confs:
                        name = conf["metadata"]["name"]
                        names = old_config_map.get(kind, [])
                        if name in names:
                            names.remove(name)

                        if kind == "Service":
                            pod_name = name
                        res = self.read(kind, name, namespace)
                        if hasattr(res, "status") and res.status == 404 and conf:
                            self.create(kind, name, namespace, conf)
                        elif not isinstance(res, ApiException) and res.metadata:
                            if res.metadata.labels:
                                config_version = res.metadata.labels.get(
                                    "config_version", 1
                                )
                            else:
                                config_version = 1

                            if config_version != conf.get("metadata").get(
                                "labels", {}
                            ).get("config_version", 1):
                                self.patch(kind, name, namespace, conf)

                    if (
                        old_config_map
                        and type(old_config_map) is dict
                        and kind in old_config_map
                        and name in old_config_map[kind]
                    ):
                        old_config_map.get(kind, []).remove(name)

                    for to_be_removed in old_config_map.get(kind, []):
                        res = self.read(kind, to_be_removed, namespace)
                        if not isinstance(res, ApiException) and res.metadata:
                            if (
                                kind not in UNSAFE_KINDS
                                or unsafe_paraphrase == UNSAFE_PARAPHRASE
                            ):
                                self.delete(kind, to_be_removed, namespace)
                            else:
                                logger.info(
                                    f"You don't have permission to delete `{kind}` for `{to_be_removed}` with namespace `{namespace}`!"
                                )

                if self.kubernetes.is_running(pod_name, namespace):
                    logger.info(
                        f"Pod state is running. Trying to Restart {svc_name}..."
                    )
                    svc.reset(hook)
            else:
                logger.info(f"Restarting {svc_name}...")
                svc.reset(hook)

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

    ###################################################
    #                 ACTION MANAGER                  #
    ###################################################
    def load_action_config(self, config, name):
        """
        Load the config for an action
        """
        return load_action_config(config, name)

    def load_actions(self, name, mode):
        """
        Load an action as local, module or remote.
        """
        # Using module for local
        mode = "module" if mode == "local" else mode

        if mode == "module":
            self.actions_optimizer.load_action_module(name)
        elif mode == "remote":
            self.actions_optimizer.load_action_remote(name)

    def unload_actions(self, name, mode, retire_svc):
        """
        Unload an action
        """
        # We are using module for local
        mode = "module" if mode == "local" else mode
        if mode == "auto":
            res = self.actions_optimizer.unload_action_auto(name)
            if not res[0]:
                return res
            if retire_svc:
                self.retire_uservice(name)
            return res
        elif mode == "module":
            return self.actions_optimizer.unload_action_module(name)
        elif mode == "remote":
            res = self.actions_optimizer.unload_action_remote(name)
            if not res[0]:
                return res
            if retire_svc:
                self.retire_uservice(name)
            return res
        else:
            return (False, f"Unrecognized action mode {mode}.")

    def retire_uservice(self, name):
        """
        Retire a remote microservice for the action.
        """
        self.actions_optimizer.retire_remote(name)

    def get_actions_status(self, name=""):
        """
        Return the status of the action
        """
        return self.actions_optimizer.get_actions_status(name)

    def actions_tracking_start(self):
        """ """
        self.actions_history["active"] = True
        self.actions_history["history"] = [{"ts": time.time()}]
        self.actions_calls.clear()

    def actions_tracking_stop(self):
        """ """
        if not self.actions_history["active"]:
            return []

        self.actions_optimizer.summarize_action_calls()

        return self.actions_history["history"]

    def benchmark_start(self):
        """
        Put JSORC under benchmark mode.
        """
        self.benchmark["jsorc"]["active"] = True
        self.benchmark["jsorc"]["requests"] = {}
        self.benchmark["jsorc"]["start_ts"] = time.time()

    def state_tracking_start(self):
        """
        Ask JSORC to start tracking the state of the system as observed by JSORC on every interval.
        """
        self.system_states = {"active": True, "states": []}

    def state_tracking_stop(self):
        """
        Stop state tracking for JSORC
        """
        ret = self.system_states
        self.system_states = {"active": True, "states": []}
        return ret

    def state_tracking_report(self):
        """
        Return state tracking history so far
        """
        return self.system_states

    def record_system_state(self):
        """
        Record system state
        """
        if self.system_states["active"]:
            ts = int(time.time())
            prom_profile = self.prometheus.info(
                namespace=self.namespace,
                exclude_prom=True,
                timestamp=ts,
                duration=self.backoff_interval,
            )
            self.system_states["states"].append(
                {
                    "ts": ts,
                    "actions": self.get_actions_status(name=""),
                    "prometheus": prom_profile,
                }
            )

    def benchmark_stop(self, report):
        """
        Stop benchmark mode and report result during the benchmark period
        """
        if not self.benchmark["jsorc"]["active"]:
            return {}

        res = self.benchmark_report()
        self.benchmark["jsorc"]["requests"] = {}
        self.benchmark["jsorc"]["active"] = False

        if report:
            return res
        else:
            return {}

    def benchmark_report(self):
        """
        Summarize benchmark results and report.
        """
        summary = {}
        duration = time.time() - self.benchmark["jsorc"]["start_ts"]
        for request, data in self.benchmark["jsorc"]["requests"].items():
            summary[request] = {}
            all_reqs = []
            for req_name, times in data.items():
                if len(times) == 0:
                    continue
                all_reqs.extend(times)
                summary[request][req_name] = {
                    "throughput": len(times) / duration,
                    "average_latency": sum(times) / len(times) * 1000,
                    "50th_latency": np.percentile(times, 50) * 1000,
                    "90th_latency": np.percentile(times, 90) * 1000,
                    "95th_latency": np.percentile(times, 95) * 1000,
                    "99th_latency": np.percentile(times, 99) * 1000,
                }
            summary[request]["all"] = {
                "throughput": len(all_reqs) / duration,
                "average_latency": sum(all_reqs) / len(all_reqs) * 1000,
                "50th_latency": np.percentile(all_reqs, 50) * 1000,
                "90th_latency": np.percentile(all_reqs, 90) * 1000,
                "95th_latency": np.percentile(all_reqs, 95) * 1000,
                "99th_latency": np.percentile(all_reqs, 99) * 1000,
            }

        return summary

    def record_state(self):
        """
        Record the current state of the system observed by JSORC
        """

    def add_to_benchmark(self, request_type, request, request_time):
        """
        Add requests to benchmark performance tracking
        """
        for bm in self.benchmark.values():
            if request_type not in bm["requests"]:
                bm["requests"][request_type] = {"_default_": []}
            if request_type == "walker_run":
                walker_name = dict(request.data)["name"]
                if walker_name not in bm["requests"][request_type]:
                    bm["requests"][request_type][walker_name] = []
                bm["requests"][request_type][walker_name].append(request_time)
            else:
                bm["requests"][request_type]["_default_"].append(request_time)

    def set_action_policy(self, policy_name, policy_params):
        """
        Set an action optimizer policy
        """
        return self.actions_optimizer.set_action_policy(policy_name, policy_params)

    def get_action_policy(self):
        """
        Get the current action optimization policy
        """
        return self.actions_optimizer.get_action_policy()

    def pre_action_call_hook(self, *args):
        pass

    def post_action_call_hook(self, *args):
        action_name = args[0]
        action_time = args[1]
        if action_name not in self.actions_calls:
            self.actions_calls[action_name] = []

        self.actions_calls[action_name].append(action_time)

    def pre_request_hook(self, *args):
        pass

    def post_request_hook(self, *args):
        request_type = args[0]
        request = args[1]
        request_time = args[2]
        if self.benchmark["jsorc"]["active"]:
            self.add_to_benchmark(request_type, request, request_time)

    def optimize(self, jsorc_interval):
        self.actions_optimizer.run(jsorc_interval)


class MetaProperties:
    def __init__(self, cls):
        self.cls = cls

        if not hasattr(cls, "_app"):
            setattr(cls, "_app", None)
            setattr(cls, "_enabled", True)
            setattr(cls, "_state", Ss.NOT_STARTED)
            setattr(cls, "_quiet", False)
            setattr(cls, "_running_interval", 0)

    @property
    def app(self) -> JsOrc:
        return self.cls._app

    @app.setter
    def app(self, val: JsOrc):
        self.cls._app = val

    @property
    def state(self) -> Ss:
        return self.cls._state

    @state.setter
    def state(self, val: Ss):
        self.cls._state = val

    @property
    def enabled(self) -> bool:
        return self.cls._enabled

    @enabled.setter
    def enabled(self, val: bool):
        pass

    @property
    def quiet(self) -> bool:
        return self.cls._quiet

    @quiet.setter
    def quiet(self, val: bool):
        pass

    @property
    def running_interval(self) -> int:
        return self.cls._running_interval

    @running_interval.setter
    def running_interval(self, val: int):
        self.cls._running_interval = val
