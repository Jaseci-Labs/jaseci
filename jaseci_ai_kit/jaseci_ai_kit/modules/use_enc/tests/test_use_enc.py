from jaseci.utils.test_core import CoreTest
from importlib import import_module


class UseEncTest(CoreTest):
    fixture_src = __file__

    import_module("jaseci_ai_kit.use_enc")

    # def setUp(self):
    #     import_module("jaseci_ai_kit.use_enc")
    #     self.log("imported")
    #     return super().setUp()

    # def tearDown(self):
    #     # un import the module
    #     import sys
    #     x = sys.modules.pop("jaseci_ai_kit.use_enc")
    #     self.log(x)
    #     return super().tearDown()

    def test_enc_text_similarity(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("use_enc.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_enc_text_similarity"}])
        # self.log(ret["report"][0])
        self.assertEqual(round(ret["report"][0], 2), 0.03)

    def test_enc_text_classify(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("use_enc.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_enc_text_classify"}])
        # self.log(ret["report"][0])
        self.assertEqual(ret["report"][0]["match"], "getdirections")

    def test_enc_get_embeddings(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("use_enc.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_enc_get_embeddings"}])
        # self.log(ret["report"][0])
        self.assertEqual(len(ret["report"][0][0]), 512)
