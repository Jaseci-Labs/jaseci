from kubernetes import client, config
from kubernetes.client.rest import ApiException
import yaml


class KubeController:
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    app_api = client.AppsV1Api()

    def get_pod_list(self):
        print("Listing pods with their IPs:")
        ret = self.api_instance.list_pod_for_all_namespaces(watch=False)
        res = []
        for i in ret.items:
            print(
                "%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name)
            )
            res.append(i.metadata)
        return res

    def create_jaseci_redis_deployment(self, config: dict, namespace: str = "default"):
        print(config)
        return self.app_api.create_namespaced_deployment(
            namespace=namespace, body=config
        )

    def kill_jaseci_redis_pod(self, name: str, namespace: str = "default"):
        try:
            api_response = self.app_api.delete_namespaced_deployment(
                name=name, namespace=namespace
            )
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


if __name__ == "__main__":
    k = KubeController()
    k.create_jaseci_redis_deployment(yaml.safe_load(open("jaseci.yaml", "r")))
    # k.kill_jaseci_redis_pod("jaseci-redis")
