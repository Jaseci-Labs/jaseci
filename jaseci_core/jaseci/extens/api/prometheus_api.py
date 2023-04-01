"""
Prometheus APIs
"""
from jaseci.extens.api.interface import Interface
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.prome_svc import PrometheusService


def prome():
    return JsOrc.svc("prome").poke(PrometheusService)


class PrometheusApi:
    """
    Prometheus APIs
    """

    @Interface.admin_api()
    def prometheus_metrics_list(self):
        """
        Return list of availabel metrics
        """
        return prome().all_metrics()

    @Interface.admin_api()
    def prometheus_pod_list(self, namespace: str = "", exclude_prom: bool = False):
        """
        Return list of pods. If exclude_prom,
        """
        return prome().pods(namespace=namespace, exclude_prom=exclude_prom)

    @Interface.admin_api()
    def prometheus_pod_info(
        self,
        namespace: str = "",
        exclude_prom: bool = False,
        timestamp: int = 0,
        duration: int = 0,
    ):
        """
        Return pods info and metrics
        """
        return (
            prome()
            .info(
                namespace=namespace,
                exclude_prom=exclude_prom,
                timestamp=timestamp,
                duration=duration,
            )
            .pod
        )

    @Interface.admin_api()
    def prometheus_node_info(
        self,
        namespace: str = "",
        exclude_prom: bool = False,
        timestamp: int = 0,
        duration: int = 0,
    ):
        """
        Return pods info and metrics
        """
        return (
            prome()
            .info(
                namespace=namespace,
                exclude_prom=exclude_prom,
                timestamp=timestamp,
                duration=duration,
            )
            .node
        )
