import unittest

from jaseci_serv.svc import RedisService


def skip_without_redis(test):
    """
    Skip test if expected not to work without redis.
    """

    def skipper(*args, **kwargs):
        if not RedisService().is_running():
            raise unittest.SkipTest("No Redis!")
        test(*args, **kwargs)

    return skipper
