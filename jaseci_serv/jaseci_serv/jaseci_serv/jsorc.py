from kubernetes import client, config
from kubernetes.client.rest import ApiException

config.load_kube_config()  # or config.load_kube_config()

configuration = client.Configuration()

with client.ApiClient(configuration) as api_client:
    api_instance = client.CoreV1Api()

    namespace = "default"  # str | see @Max Lobur's answer on how to get this
    name = "jaseci-redis-5f98d98bc4-dmxch"  # str | Pod name, e.g. via api_instance.list_namespaced_pod(namespace)

    try:
        api_response = api_instance.delete_namespaced_pod(name, namespace)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
