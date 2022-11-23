KUBERNETES_CONFIG = {"in_cluster": True, "config": None}

META_CONFIG = {
    "automation": False,
    "interval": 10,
    "namespace": "default",
    "keep_alive": ["promon", "redis", "task", "mail"],
    "kubernetes": KUBERNETES_CONFIG,
}
