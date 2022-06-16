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


def create_jaseci_redis_deployment():
    with open("jaseci.yaml", "r") as f:
        dep_yaml = yaml.safe_load(f)
        res = app_api.create_namespaced_deployment(namespace="default", body=dep_yaml)
        print(res)


def kill_jaseci_redis_pod():
    namespace = ""
    name = ""

    for i in get_pod_list():
        if i.name.startswith("jaseci-redis"):
            name = i.name
            namespace = i.namespace
            break

    try:
        api_response = app_api.delete_namespaced_deployment(
            name="jaseci-redis", namespace="default"
        )
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


if __name__ == "__main__":
    create_jaseci_redis_deployment()
    # kill_jaseci_redis_pod()
