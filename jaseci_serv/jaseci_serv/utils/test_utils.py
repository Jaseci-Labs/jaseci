import unittest
from jaseci.app.redis.redis_app import redis_app


def skip_without_redis(test):
    """
    Skip test if expected not to work without redis.
    """

    def skipper(*args, **kwargs):

        if not redis_app().is_running():
            raise unittest.SkipTest("No Redis!")

    return skipper
