from jaseci.utils.utils import logger
from .promon import Promon
import time
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import yaml
import multiprocessing


class KubeController:
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
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


class Monitor:
    def __init__(self, promonUrl: str, k8sconfig):
        self.promon = Promon(promonUrl)
        self.controller = KubeController(k8sconfig)

    def strategy_start_redis(self):
        deployments = self.controller.get_deployment_list()
        exsits = False
        for deployment in deployments:
            if deployment["name"] == "jaseci-redis":
                exsits = True
        if not exsits:
            self.controller.create_deployment(
                config=yaml.safe_load(open("jaseci.yaml", "r"))
            )

    def strategy_redis_cpu(self, nodeName: str, deploymentNameSpace: str, deploymentName: str):
        cpu = self.promon.cpu_utilization_percentage()
        cpu_usage = cpu[nodeName]
        print(f"Detect CPU Usage: {cpu_usage}")
        if cpu_usage > 10:
            pods = self.controller.get_deployment_list()
            for pod in pods:
                namespace = pod["namespace"]
                name = pod["name"]
                if name == deploymentName:
                    print("Kill deployment")
                    self.controller.kill_deployment(name=name, namespace=namespace)
        if cpu_usage < 5:
            pods = self.controller.get_deployment_list()
            redisRunning = False
            for pod in pods:
                if pod["name"] == deploymentName:
                    redisRunning = True
            if not redisRunning:
                print("Creating new deployment")
                self.controller.create_deployment(
                    config=yaml.safe_load(open("jaseci.yaml", "r"))
                )

    def strategy_service_cpu(self):
        cpu = self.promon.cpu_utilization_per_pod_cores()
        count = 0
        total = 0
        for podName in cpu.keys():
            if podName.startswith("jaseci-redis"):
                count = count + 1
                total = total + cpu[podName]

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

def daemon(k8sConf, prometheusURL: str):
    m = Monitor(prometheusURL, k8sConf)
    while True:
        # m.strategy_redis_cpu("minikube", "default", "jaseci-redis")
        m.strategy_start_redis()
        time.sleep(10)

def startMonitoring(k8sConf, prometheusURL: str):
    monitor = multiprocessing.Process(target = daemon, args = (k8sConf, prometheusURL))
    monitor.start()
    return monitor

def waitMonitoring(monitorThread):
    monitorThread.join()

def stopMonitoring(monitorThread):
    monitorThread.terminate()

def remoteK8sConf(K8sURL: str):
    k8sconf = client.Configuration()
    k8sconf.host = K8sURL
    k8sconf.verify_ssl = False
    return k8sconf

def inclusterK8sConf():
    return config.load_incluster_config()

monitorThread = startMonitoring(k8sConf = inclusterK8sConf(), prometheusURL = "http://js-prometheus:9090")
logger.info("Started Monitoring")
waitMonitoring(monitorThread)
