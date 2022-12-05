import unittest

from jaseci_serv.svc import MetaService


def skip_without_redis(test):
    """
    Skip test if expected not to work without redis.
    """

    def skipper(*args, **kwargs):
        redis = MetaService().get_service("redis")
        if not redis.is_running():
            raise unittest.SkipTest("No Redis!")
        test(*args, **kwargs)

    return skipper


def skip_without_kube(test):
    """
    Skip test if expected not to work without access to a kubernete cluster
    """

    def skipper(*args, **kwargs):
        meta = MetaService()
        if not meta.in_cluster():
            raise unittest.SkipTest("Jaseci not in a kubernetes context!")
        test(*args, **kwargs)

    return skipper
