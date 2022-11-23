import sys

KUBERNETES_CONFIG = {"in_cluster": False, "config": None}

META_CONFIG = {"automation": False, "monitoring": True, "kubernetes": KUBERNETES_CONFIG}

RUN_SVCS = "test" in sys.argv or "runserver" in sys.argv
