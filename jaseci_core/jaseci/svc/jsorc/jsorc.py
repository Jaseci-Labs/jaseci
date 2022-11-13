from time import sleep

from kubernetes.client.rest import ApiException
from jaseci.utils.utils import logger
from jaseci.svc import CommonService, ServiceState as Ss
from jaseci.svc.kubernetes import Kube
from jaseci.svc.actions_optimizer.actions_optimizer import ActionsOptimizer
from .config import JSORC_CONFIG

#################################################
#                  JASECI ORC                   #
#################################################


class JsOrcService(CommonService):

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        self.interval = 10
        self.namespace = "default"
        self.keep_alive = []

        super().__init__(hook)

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.interval = self.config.get("interval", 10)
        self.namespace = self.config.get("namespace", "default")
        self.keep_alive = self.config.get("keep_alive", [])

        self.app = JsOrc(hook.meta, hook.kube.app, self.quiet)
        self.state = Ss.RUNNING
        # self.app.check(self.namespace, "redis")
        self.spawn_daemon(jsorc=self.interval_check)

    def interval_check(self):
        while True:
            # Keeping set of services alive
            for svc in self.keep_alive:
                try:
                    self.app.check(self.namespace, svc)
                except Exception as e:
                    logger.error(
                        f"Error checking {svc} !\n" f"{e.__class__.__name__}: {e}"
                    )

            self.app.optimize(jsorc_interval=self.interval)

            sleep(self.interval)

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def reset(self, hook):
        self.terminate_daemon("jsorc")
        super().reset(hook)

    def failed(self):
        super().failed()
        self.terminate_daemon("jsorc")

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def build_config(self, hook) -> dict:
        return hook.service_glob("JSORC_CONFIG", JSORC_CONFIG)


# ----------------------------------------------- #


class JsOrc:
    def __init__(self, meta, kube: Kube, quiet: bool):
        self.meta = meta
        self.kube = kube
        self.quiet = quiet
        # overall performance tracking benchmark
        self.benchmark = {
            "jsorc": {"active": False, "requests": {}},
            "actions_optimizer": {"active": False, "requests": {}},
        }
        self.actions_optimizer = ActionsOptimizer(
            kube=kube, policy="default", benchmark=self.benchmark["actions_optimizer"]
        )

    def is_running(self, name: str, namespace: str):
        try:
            return (
                self.kube.core.list_namespaced_pod(
                    namespace=namespace, label_selector=f"pod={name}"
                )
                .items[0]
                .status.phase
                == "Running"
            )
        except Exception:
            return False

    def create(self, kind: str, name: str, namespace: str, conf: dict):
        try:
            if not self.quiet:
                logger.info(
                    f"Creating {kind} for `{name}` with namespace `{namespace}`"
                )
                # HACK
                if kind == "DaemonSet" and name == "jaseci-prometheus-node-exporter":
                    # TODO: temporary hack until we figure out why kube config from the python file is not updating
                    del conf["spec"]["template"]["spec"]["containers"][0][
                        "volumeMounts"
                    ][2]["mountPropagation"]
                    conf["spec"]["template"]["spec"]["containers"][0][
                        "hostRootFsMount"
                    ] = {"enabled": False, "mountPropagation": "HostToContainer"}
                    conf["spec"]["template"]["spec"]["containers"][0][
                        "hostRootFs"
                    ] = False

            self.kube.create(kind, namespace, conf)
        except ApiException:
            if not self.quiet:
                logger.error(
                    f"Error creating {kind} for `{name}` with namespace `{namespace}`"
                )

    def read(self, kind: str, name: str, namespace: str):
        try:
            return self.kube.read(kind, name, namespace=namespace)
        except ApiException as e:
            if not self.quiet:
                logger.error(
                    f"Error retrieving {kind} for `{name}` with namespace `{namespace}`"
                )
            return e

    # TODO: should we have a separate and dedicated benchmark service?
    def benchmark_start(self):
        """
        Put JSORC under benchmark mode.
        """
        self.benchmark["jsorc"]["active"] = True
        self.benchmark["jsorc"]["requests"] = {}

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
        for request, times in self.benchmark["jsorc"]["requests"].items():
            summary[request] = {"average_latency": sum(times) / len(times)}

        return summary

    def add_to_benchmark(self, request_type, request_time):
        """
        Add requests to benchmark performance tracking
        """
        for bm in self.benchmark.values():
            if request_type not in bm["requests"]:
                bm["requests"][request_type] = []
            bm["requests"][request_type].append(request_time)

    def load_actions(self, name, mode):
        """
        Load an action as local, module or remote.
        """
        # We are using module for local
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
        if mode == "module":
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

    def get_actions_status(self, name):
        """
        Return the status of the action
        """
        return self.actions_optimizer.get_actions_status(name)

    def set_action_policy(self, policy_name):
        """
        Set an action optimizer policy
        """
        return self.actions_optimizer.set_action_policy(policy_name)

    def get_action_policy(self):
        """
        Get the current action optimization policy
        """
        return self.actions_optimizer.get_action_policy()

    def manage_actions(self, name):
        self.actions_optimizer.load_action(name, mode="auto")

    def pre_action_call_hook(self, *args):
        pass

    def post_action_call_hook(self, *args):
        pass

    def pre_request_hook(self, *args):
        pass

    def post_request_hook(self, *args):
        request_type = args[0]
        request_time = args[1]
        if self.benchmark["jsorc"]["active"]:
            self.add_to_benchmark(request_type, request_time)

    def optimize(self, jsorc_interval):
        self.actions_optimizer.run(jsorc_interval)

    def check(self, namespace, svc):

        svc = self.meta.get_service(svc)

        if not svc.is_running():
            if svc.kube:
                config_map = svc.kube
                pod_name = ""
                for kind, confs in config_map.items():
                    for conf in confs:
                        name = conf["metadata"]["name"]
                        if kind == "Service":
                            pod_name = name
                        res = self.read(kind, name, namespace)
                        if hasattr(res, "status") and res.status == 404 and conf:
                            self.create(kind, name, namespace, conf)

                if self.is_running(pod_name, namespace):
                    res = self.read("Endpoints", pod_name, namespace)
                    if res.metadata:
                        svc.reset(self.meta.build_hook())
            else:
                svc.reset(self.meta.build_hook())
