import os
from unittest import TestCase

from jaseci.svc import MetaService
from jaseci.utils.utils import TestCaseHelper


class CoreTest(TestCaseHelper, TestCase):
    """Unit tests for Jac Core APIs"""

    fixture_src = __file__

    def setUp(self, run_svcs=False):
        super().setUp()
        self.meta = MetaService(run_svcs=run_svcs)
        self.smast = self.meta.build_super_master()
        self.mast = self.meta.build_master(h=self.smast._h)

    def tearDown(self):
        super().tearDown()

    def call(self, mast, pl):
        ret = mast.general_interface_to_api(api_name=pl[0], params=pl[1])
        return ret

    def load_jac(self, fn):
        with open(os.path.dirname(self.fixture_src) + "/fixtures/" + fn) as f:
            return f.read()
