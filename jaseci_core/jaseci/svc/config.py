import os

KUBERNETES_CONFIG = {"in_cluster": True, "config": None}

META_CONFIG = {
    "automation": os.environ.get("JSORC_AUTOMATION") == "true",
    "backoff_interval": 10,
    "namespace": "default",
    "keep_alive": ["database", "promon", "redis", "task", "mail", "elastic"],
    "kubernetes": KUBERNETES_CONFIG,
}
