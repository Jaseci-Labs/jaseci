KUBERNETES_CONFIG = {"in_cluster": True, "config": None}

META_CONFIG = {
    "automation": False,
    "backoff_interval": 10,
    "namespace": "default",
    "keep_alive": ["promon", "redis", "task", "mail", "elastic"],
    "kubernetes": KUBERNETES_CONFIG,
}
