import unittest

from jaseci import JsOrc
from jaseci.svc.kube_svc import KubeService


def skip_without_redis(test):
    """
    Skip test if expected not to work without redis.
    """

    def skipper(*args, **kwargs):
        if not JsOrc.svc("redis").is_running():
            raise unittest.SkipTest("No Redis!")
        test(*args, **kwargs)

    return skipper


def skip_without_kube(test):
    """
    Skip test if expected not to work without access to a kubernete cluster
    """

    def skipper(*args, **kwargs):
        kube = JsOrc.svc("kube", KubeService)
        if not kube.is_running() or not kube.in_cluster():
            raise unittest.SkipTest("Jaseci not in a kubernetes context!")
        test(*args, **kwargs)

    return skipper
