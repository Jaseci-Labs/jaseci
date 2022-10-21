from jaseci.utils.test_core import CoreTest


class VectorTest(CoreTest):
    """UnitTest for Vector Module"""

    fixture_src = __file__

    def test_get_centroid(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("vector.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "get_centroid_test"}])
        ret = [ret["report"][0][0], round(ret["report"][0][1], 3)]
        self.assertEqual(ret, [[1.0, 2.0, 3.5], 0.998])

    def test_softmax(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("vector.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "softmax_test"}])
        ret = [round(num, 2) for num in ret["report"][0]]
        self.assertEqual(ret, [0.09, 0.24, 0.67])

    def test_dot_product(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("vector.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "dot_product_test"}])
        self.assertEqual(ret["report"][0], 17)

    def test_cosine_similarity_single(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("vector.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "cosine_similarity_test"}])
        ret = round(ret["report"][0], 3)
        self.assertEqual(ret, 0.991)

    def test_cosine_similarity_batch(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("vector.jac")}],
        )
        ret = self.call(
            self.mast, ["walker_run", {"name": "cosine_similarity_batch_test"}]
        )
        ret = [round(num, 2) for num in ret["report"][0]]
        self.assertEqual(ret, [0.99, 1.0])
