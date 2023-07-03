from jaseci.utils.test_core import CoreTest, jac_testcase


class MathsTests(CoreTest):
    """UnitTest for Regex Module"""

    fixture_src = __file__

    @jac_testcase("maths.jac", "ceil_test")
    def test_ceil(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 124)

    @jac_testcase("maths.jac", "comb_test")
    def test_comb(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 4950)

    @jac_testcase("maths.jac", "copysign_test")
    def test_copysign(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, -100.0)

    @jac_testcase("maths.jac", "fabs_test")
    def test_fabs(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 10.0)

    @jac_testcase("maths.jac", "factorial_test")
    def test_factorial(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 3628800)

    @jac_testcase("maths.jac", "floor_test")
    def test_floor(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 10)

    @jac_testcase("maths.jac", "fmod_test")
    def test_fmod(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 1.0)
