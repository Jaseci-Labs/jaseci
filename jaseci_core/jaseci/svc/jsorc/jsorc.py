from .promon.promon import Promon
import time
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os
import yaml
import multiprocessing
from jaseci.utils.utils import logger


class KubeController:
    # A set of all functions that are helpful for kubernetes operations
    # Configs can be set in Configuration class directly or using helper utility

    def __init__(self, configuration):
        self.config = configuration
        self.api_instance = client.CoreV1Api(self.config)
        self.app_client = client.ApiClient(self.config)
        self.app_api = client.AppsV1Api(self.app_client)

    def get_pod_list(self):
        ret = self.api_instance.list_pod_for_all_namespaces(watch=False)
        res = []
        for i in ret.items:
            res.append({"namespace": i.metadata.namespace, "name": i.metadata.name})
        return res

    def get_deployment_list(self):
        ret = self.app_api.list_deployment_for_all_namespaces(watch=False)
        res = []
        for i in ret.items:
            res.append({"namespace": i.metadata.namespace, "name": i.metadata.name})
        return res

    def create_deployment(self, config: dict, namespace: str = "default"):
        return self.app_api.create_namespaced_deployment(
            namespace=namespace, body=config
        )

    def get_deployment_conf(self, name: str, namespace: str = "default"):
        api_response = self.app_api.read_namespaced_deployment(
            name=name, namespace=namespace
        )
        return api_response

    def patch_deployment_conf(self, config, name: str, namespace: str = "default"):
        api_response = self.app_api.patch_namespaced_deployment(
            name=name, namespace=namespace, body=config
        )
        return api_response

    def deployment_set_scale(
        self, name: str, namespace: str = "default", scale: int = 1
    ):
        # This is just a small shortcut to set the scale of a deployment
        conf = self.get_deployment_conf(name, namespace)
        conf.spec.replicas = scale
        self.patch_deployment_conf(conf, name, namespace)

    def kill_deployment(self, name: str, namespace: str = "default"):
        try:
            api_response = self.app_api.delete_namespaced_deployment(
                name=name, namespace=namespace
            )
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


class Monitor:
    def __init__(self, promon_url: str, k8sconfig):
        self.promon = Promon(promon_url)
        self.controller = KubeController(k8sconfig)

    def strategy_start_redis(self):
        deployments = self.controller.get_deployment_list()
        exsits = False
        for deployment in deployments:
            if deployment["name"] == "jaseci-redis":
                exsits = True
        if not exsits:
            logger.info("Creating new jaseci redis")
            dirpath = os.path.dirname(os.path.realpath(__file__))
            filepath = os.path.join(dirpath, "jaseci-redis.yaml")
            self.controller.create_deployment(
                config=yaml.safe_load(open(filepath, "r"))
            )

    def strategy_redis_cpu(
        self, node_name: str, deployment_namespace: str, deployment_name: str
    ):
        cpu = self.promon.cpu_utilization_percentage()
        cpu_usage = cpu[node_name]
        print(f"Detect CPU Usage: {cpu_usage}")
        if cpu_usage > 10:
            pods = self.controller.get_deployment_list()
            for pod in pods:
                namespace = pod["namespace"]
                name = pod["name"]
                if name == deployment_name:
                    print("Kill deployment")
                    self.controller.kill_deployment(name=name, namespace=namespace)
        if cpu_usage < 5:
            pods = self.controller.get_deployment_list()
            redis_running = False
            for pod in pods:
                if pod["name"] == deployment_name:
                    redis_running = True
            if not redis_running:
                print("Creating new deployment")
                self.controller.create_deployment(
                    config=yaml.safe_load(open("jaseci.yaml", "r"))
                )

    def strategy_service_cpu(self):
        cpu = self.promon.cpu_utilization_per_pod_cores()
        count = 0
        total = 0
        for pod_name in cpu.keys():
            if pod_name.startswith("jaseci-redis"):
                count = count + 1
                total = total + cpu[pod_name]

        avg = total / count
        print(avg)
        if avg > 0.001:
            conf = self.controller.get_deployment_conf("jaseci-redis", "default")
            replicas = conf.spec.replicas + 1
            print(f"Num of Replicas: {replicas}")
            self.controller.deployment_set_scale("jaseci-redis", "default", replicas)
        if avg < 0.001:
            conf = self.controller.get_deployment_conf("jaseci-redis", "default")
            replicas = conf.spec.replicas - 1
            print(f"Num of Replicas: {replicas}")
            self.controller.deployment_set_scale("jaseci-redis", "default", replicas)


def daemon(k8s_conf, prometheus_url: str):
    m = Monitor(prometheus_url, k8s_conf)
    while True:
        # m.strategy_redis_cpu("minikube", "default", "jaseci-redis")
        m.strategy_start_redis()
        time.sleep(10)


def start_monitoring(k8s_conf, prometheus_url: str):
    monitor = multiprocessing.Process(target=daemon, args=(k8s_conf, prometheus_url))
    monitor.start()
    return monitor


def wait_monitoring(monitor_thread):
    monitor_thread.join()


def stop_monitoring(monitor_thread):
    monitor_thread.terminate()


def remote_k8s_conf(k8s_url: str):
    k8sconf = client.Configuration()
    k8sconf.host = k8s_url
    k8sconf.verify_ssl = False
    return k8sconf


def incluster():
    try:
        config.load_incluster_config()
    except config.config_exception.ConfigException:
        return False
    return True


def jsorc_start():
    logger.info("JSORC Running")
    if incluster():
        k8s_config = None
        start_monitoring(
            k8s_conf=k8s_config, prometheus_url="http://js-prometheus:9090"
        )
        logger.info("Monitoring started")
