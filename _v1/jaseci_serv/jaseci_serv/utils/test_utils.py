import unittest

from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.kube_svc import KubeService


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
