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

    @jac_testcase("maths.jac", "gcd_test")
    def test_gcd(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 1)

    @jac_testcase("maths.jac", "isclose_test")
    def test_isclose(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, False)

    @jac_testcase("maths.jac", "isfinite_test")
    def test_isfinite(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, True)

    @jac_testcase("maths.jac", "isinf_test")
    def test_isinf(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, False)

    @jac_testcase("maths.jac", "isnan_test")
    def test_isnan(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, False)

    @jac_testcase("maths.jac", "isqrt_test")
    def test_isqrt(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 3)

    @jac_testcase("maths.jac", "lcm_test")
    def test_lcm(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 420)

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

    @jac_testcase("maths.jac", "prod_test")
    def test_prod(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 120)

    @jac_testcase("maths.jac", "remainder_test")
    def test_remainder(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 3.0)

    @jac_testcase("maths.jac", "trunc_test")
    def test_trunc(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 23)

    @jac_testcase("maths.jac", "trunc_test")
    def test_trunc(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 23)

    @jac_testcase("maths.jac", "ulp_test")
    def test_ulp(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 3.552713678800501e-15)

    @jac_testcase("maths.jac", "cubert_test")
    def test_cubert(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 3.0)

    @jac_testcase("maths.jac", "exp_test")
    def test_exp(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 532048240601.79865)

    @jac_testcase("maths.jac", "log_test")
    def test_log(self, ret):
        ret = ret["report"][0]
        self.assertEqual(ret, 1.4313637641589871)
