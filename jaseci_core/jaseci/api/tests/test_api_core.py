from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.element.super_master import super_master
from jaseci.element.master import master
from jaseci.utils.mem_hook import mem_hook
import os


class core_test(TestCaseHelper, TestCase):
    """Unit tests for Jac Core APIs"""

    def setUp(self):
        super().setUp()
        self.smast = super_master(h=mem_hook())
        self.mast = master(h=self.smast._h)

    def tearDown(self):
        super().tearDown()

    def call(self, mast, pl):
        ret = mast.general_interface_to_api(api_name=pl[0], params=pl[1])
        return ret

    def load_jac(self, fn):
        with open(os.path.dirname(__file__) + "/fixtures/" + fn) as f:
            return f.read()
