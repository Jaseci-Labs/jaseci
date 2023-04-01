from jaseci.utils.test_core import CoreTest, jac_testcase


class VectorTest(CoreTest):
    """UnitTest for Vector Module"""

    fixture_src = __file__

    @jac_testcase("vector.jac", "get_centroid_test")
    def test_get_centroid(self, ret):
        ret = [ret["report"][0][0], round(ret["report"][0][1], 3)]
        self.assertEqual(ret, [[1.0, 2.0, 3.5], 0.998])

    @jac_testcase("vector.jac", "softmax_test")
    def test_softmax(self, ret):
        ret = [round(num, 2) for num in ret["report"][0]]
        self.assertEqual(ret, [0.09, 0.24, 0.67])

    @jac_testcase("vector.jac", "dot_product_test")
    def test_dot_product(self, ret):
        self.assertEqual(ret["report"][0], 17)

    @jac_testcase("vector.jac", "cosine_similarity_test")
    def test_cosine_similarity_single(self, ret):
        ret = round(ret["report"][0], 3)
        self.assertEqual(ret, 0.991)

    @jac_testcase("vector.jac", "cosine_similarity_batch_test")
    def test_cosine_similarity_batch(self, ret):
        ret = [round(num, 2) for num in ret["report"][0]]
        self.assertEqual(ret, [0.99, 1.0])

    @jac_testcase("vector.jac", "dimensionality_reduction_test")
    def test_dimensionality_reduction(self, ret):
        ret = len(ret["report"][0][0])
        self.assertEqual(ret, 2)
