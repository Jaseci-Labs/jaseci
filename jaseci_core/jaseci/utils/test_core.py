import os
from unittest import TestCase

from jaseci.svc import MetaService
from jaseci.utils.utils import TestCaseHelper


class CoreTest(TestCaseHelper, TestCase):
    """Unit tests for Jac Core APIs"""

    fixture_src = __file__

    def setUp(self):
        super().setUp()
        self.meta = MetaService()
        self.smast = self.meta.super_master()
        self.mast = self.meta.master(h=self.smast._h)

    def tearDown(self):
        super().tearDown()

    def call(self, mast, pl):
        ret = mast.general_interface_to_api(api_name=pl[0], params=pl[1])
        return ret

    def load_jac(self, fn):
        with open(os.path.dirname(self.fixture_src) + "/fixtures/" + fn) as f:
            return f.read()
