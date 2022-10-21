import unittest
from jaseci.utils.test_core import CoreTest
from jaseci.actions.live_actions import load_module_actions, load_local_actions


class UseEncTest(CoreTest):
    fixture_src = __file__

    ret = load_module_actions("jaseci_ai_kit.use_enc")
    assert ret == True

    def test_load_local_actions(self):
        ret = load_local_actions("jaseci_ai_kit/modules/use_enc/use_enc.py")
        self.assertEqual(ret, True)

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
