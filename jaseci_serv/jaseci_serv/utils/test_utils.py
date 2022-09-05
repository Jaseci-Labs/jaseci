import unittest
from jaseci.utils.redis_hook import redis_hook as rh


def skip_without_redis(test):
    """
    Skip test if expected not to work without redis.
    """

    def skipper(*args, **kwargs):
        if not rh.redis_running():
            raise unittest.SkipTest("No Redis!")

    return skipper
