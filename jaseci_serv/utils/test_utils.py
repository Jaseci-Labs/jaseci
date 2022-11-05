import unittest

from svc import MetaService


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
