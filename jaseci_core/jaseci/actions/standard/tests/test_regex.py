from jaseci.utils.test_core import CoreTest, jac_testcase


class VectorTest(CoreTest):
    """UnitTest for Vector Module"""

    fixture_src = __file__

    @jac_testcase("regex.jac", "findall_test")
    def findall_test(self, ret):
        self.assertEqual(ret["success"], True)
