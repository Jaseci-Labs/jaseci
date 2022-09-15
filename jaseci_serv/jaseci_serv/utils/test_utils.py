import unittest
from jaseci_serv.svc.redis.redis_svc import redis_svc


def skip_without_redis(test):
    """
    Skip test if expected not to work without redis.
    """

    def skipper(*args, **kwargs):

        if not redis_svc().is_running():
            raise unittest.SkipTest("No Redis!")

    return skipper
