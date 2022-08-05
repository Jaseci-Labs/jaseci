from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
from jaseci.element.super_master import super_master
from jaseci.element.master import master
from jaseci.utils.mem_hook import mem_hook
import jaseci.tests.jac_test_code as jtc


class core_test(TestCaseHelper, TestCase):
    """Unit tests for Jac Core APIs"""

    def setUp(self):
        super().setUp()
        self.mast = super_master(h=mem_hook())
        self.mast2 = super_master(h=self.mast._h)
        self.mast.sentinel_register(name="test", code=jtc.basic)

        self.lms = master(h=mem_hook())
        self.lms2 = master(h=self.lms._h)
        self.lms.sentinel_register(name="test", code=jtc.basic)

    def tearDown(self):
        super().tearDown()

    def call(self, mast, pl):
        ret = mast.general_interface_to_api(api_name=pl[0], params=pl[1])
        return ret
