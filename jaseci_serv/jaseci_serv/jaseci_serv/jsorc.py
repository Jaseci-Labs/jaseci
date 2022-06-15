from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
api_instance = client.CoreV1Api()


def get_pod_list():
    print("Listing pods with their IPs:")
    ret = api_instance.list_pod_for_all_namespaces(watch=False)
    res = []
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        res.append(i.metadata)
    return res


def kill_jaseci_redis_pod():
    namespace = ""
    name = ""

    for i in get_pod_list():
        if i.name.startswith("jaseci-redis"):
            name = i.name
            namespace = i.namespace
            break

    try:
        api_response = api_instance.delete_namespaced_pod(name, namespace)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


if __name__ == "__main__":
    kill_jaseci_redis_pod()
