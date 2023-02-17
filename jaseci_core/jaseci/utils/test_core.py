import os
from unittest import TestCase

from jaseci import JsOrc
from jaseci.utils.utils import TestCaseHelper


class CoreTest(TestCaseHelper, TestCase):
    """Unit tests for Jac Core APIs"""

    fixture_src = __file__

    def setUp(self):
        super().setUp()
        self.smast = JsOrc.super_master()
        self.mast = JsOrc.master(h=self.smast._h)

    def tearDown(self):
        super().tearDown()

    def call(self, mast, pl):
        ret = mast.general_interface_to_api(api_name=pl[0], params=pl[1])
        return ret

    def load_jac(self, fn):
        with open(os.path.dirname(self.fixture_src) + "/fixtures/" + fn) as f:
            return f.read()


def jac_testcase(jac_file: str, test_name: str):
    """decorator for test cases"""

    def decorator(func):
        def wrapper(self):
            self.call(
                self.mast,
                ["sentinel_register", {"code": self.load_jac(jac_file)}],
            )
            ret = self.call(self.mast, ["walker_run", {"name": test_name}])
            func(self, ret)

        return wrapper

    return decorator
