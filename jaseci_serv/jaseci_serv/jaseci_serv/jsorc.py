from promon import Promon
import time
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import yaml
import multiprocessing


class KubeController:
    # Configs can be set in Configuration class directly or using helper utility
    aconfig = client.Configuration()
    aconfig.host = "http://clarity31.eecs.umich.edu:8084"
    aconfig.verify_ssl = False

    api_instance = client.CoreV1Api(aconfig)
    app_client = client.ApiClient(aconfig)
    app_api = client.AppsV1Api(app_client)

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
        print(api_response)
        return api_response

    def patch_deployment_conf(self, config, name: str, namespace: str = "default"):
        api_response = self.app_api.patch_namespaced_deployment(
            name=name, namespace=namespace, body=config
        )
        print(api_response)

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
    def __init__(self, promonUrl: str):
        self.promon = Promon(promonUrl)
        self.controller = KubeController()

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

def daemon():
    m = Monitor("http://clarity31.eecs.umich.edu:8082")
    while True:
        m.strategy_redis_cpu("minikube", "default", "jaseci-redis")
        time.sleep(10)

def startMonitoring():
    monitor = multiprocessing.Process(target = daemon)
    monitor.start()
    return monitor

def waitMonitoring(monitorThread):
    monitorThread.join()

def stopMonitoring(monitorThread):
    monitorThread.terminate()

if __name__ == "__main__":
    monitorThread = startMonitoring()
    waitMonitoring(monitorThread)
    # m = Monitor("http://localhost:8080")
    # m.check(
    #     nodeName="minikube",
    #     deploymentName="jaseci-redis",
    #     deploymentNameSpace="default",
    # )
    # k = KubeController()
