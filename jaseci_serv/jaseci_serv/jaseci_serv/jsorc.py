from kubernetes import client, config
from kubernetes.client.rest import ApiException
import yaml

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
api_instance = client.CoreV1Api()
app_api = client.AppsV1Api()


def get_pod_list():
    print("Listing pods with their IPs:")
    ret = api_instance.list_pod_for_all_namespaces(watch=False)
    res = []
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        res.append(i.metadata)
    return res


def create_jaseci_redis_deployment(config: str, namespace: str = "default"):
    with open(config, "r") as f:
        dep_yaml = yaml.safe_load(f)
        res = app_api.create_namespaced_deployment(namespace=namespace, body=dep_yaml)
        print(res)


def kill_jaseci_redis_pod(name: str, namespace: str = "default"):
    try:
        api_response = app_api.delete_namespaced_deployment(
            name=name, namespace=namespace
        )
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


if __name__ == "__main__":
    # create_jaseci_redis_deployment("jaseci.yaml")
    kill_jaseci_redis_pod("jaseci-redis")
