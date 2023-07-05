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

    @jac_testcase("maths.jac", "frexp_test")
    def test_frexp(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, [0.78125, 7])

    @jac_testcase("maths.jac", "fsum_test")
    def test_fsum(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 18.0)

    # gcd todo

    # isclose todo

    # isfinite todo

    # isinf todo

    # isnan toto

    @jac_testcase("maths.jac", "isqrt_test")
    def test_isqrt(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 3)

    # lcm todo

    @jac_testcase("maths.jac", "ldexp_test")
    def test_isqrt(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 36.0)

    @jac_testcase("maths.jac", "modf_test")
    def test_modf(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, [0.0, 9.0])

    @jac_testcase("maths.jac", "nextafter_test")
    def test_nextafter(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 8.999999999999998)

    @jac_testcase("maths.jac", "perm_test")
    def test_perm(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 25852016738884976640000)
