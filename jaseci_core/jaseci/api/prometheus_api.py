"""
Prometheus APIs
"""
from jaseci.api.interface import Interface


class PrometheusApi:
    """
    Prometheus APIs
    """

    @Interface.admin_api()
    def prometheus_metrics_list(self):
        """
        Return list of availabel metrics
        """
        hook = self._h
        if hook.meta.run_svcs:
            return hook.promon.all_metrics()
        else:
            return {"success": False, "message": "No runnning Prometheus service."}

    @Interface.admin_api()
    def prometheus_pod_list(self, namespace: str = "", exclude_prom: bool = False):
        """
        Return list of pods. If exclude_prom,
        """
        hook = self._h
        if hook.meta.run_svcs:
            return hook.promon.pods(namespace=namespace, exclude_prom=exclude_prom)
        else:
            return {"success": False, "message": "No runnning Prometheus service."}

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
        hook = self._h
        if hook.meta.run_svcs:
            return hook.promon.info(
                namespace=namespace,
                exclude_prom=exclude_prom,
                timestamp=timestamp,
                duration=duration,
            )
        else:
            return {"success": False, "message": "No runnning Prometheus service."}
