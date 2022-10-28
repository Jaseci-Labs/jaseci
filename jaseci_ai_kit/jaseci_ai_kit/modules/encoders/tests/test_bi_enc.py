from jaseci.utils.test_core import CoreTest, jac_testcase
import unittest
import argparse


class BiEncTest(CoreTest):
    fixture_src = __file__

    def setUp(self) -> None:
        super().setUp()
        ret = self.call(
            self.smast,
            ["actions_load_module", {"mod": "jaseci_ai_kit.modules.encoders.bi_enc"}],
        )
        self.assertEqual(ret["success"], True)
        mod_list = self.call(self.smast, ["actions_module_list", {}])
        self.assertIn("jaseci_ai_kit.modules.encoders.bi_enc", mod_list)
        act_list = self.call(self.smast, ["actions_list", {}])
        act_list = [v for v in act_list if "bi_enc" in v]
        self.assertEqual(len(act_list), 14)

    @jac_testcase("bi_enc.jac", "test_bi_enc_cos_sim")
    def test_cos_sim_function(self, ret):
        self.assertEqual(round(ret["report"][0], 2), 0.91)

    @jac_testcase("bi_enc.jac", "test_bi_enc_infer")
    def test_biencoder_infer(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_context_emb")
    def test_biencoder_context_emb(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0][0]), 128)

    @jac_testcase("bi_enc.jac", "test_bi_enc_cand_emb")
    def test_biencoder_candidate_emb(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(len(ret["report"][0][0]), 128)

    @jac_testcase("bi_enc.jac", "test_bi_enc_train_config")
    def test_biencoder_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_model_config")
    def test_biencoder_model_config(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_train")
    def test_biencoder_train(self, ret):
        print(ret["report"][0])
        self.assertEqual(ret["report"][0], "Model Training is complete.")
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_save_model")
    def test_biencoder_save_model(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("bi_enc.jac", "test_bi_enc_load_model")
    def test_biencoder_load_model(self, ret):
        self.assertEqual(ret["success"], True)

    def tearDown(self) -> None:
        super().tearDown()
        ret = self.call(self.smast, ["actions_module_list", {}])
        before = len(ret)

        ret = self.call(
            self.smast,
            [
                "actions_unload_module",
                {"name": "jaseci_ai_kit.modules.encoders.bi_enc"},
            ],
        )
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertEqual(len(ret), before - 1)


def test_suite(args):
    suite = unittest.TestSuite()
    suite.addTest(BiEncTest("test_cos_sim_function"))
    suite.addTest(BiEncTest("test_biencoder_infer"))
    suite.addTest(BiEncTest("test_biencoder_context_emb"))
    suite.addTest(BiEncTest("test_biencoder_candidate_emb"))
    suite.addTest(BiEncTest("test_biencoder_train_config"))
    suite.addTest(BiEncTest("test_biencoder_model_config"))
    suite.addTest(BiEncTest("test_biencoder_train"))
    suite.addTest(BiEncTest("test_biencoder_save_model"))
    suite.addTest(BiEncTest("test_biencoder_load_model"))

    return suite


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local",
        help="Use action load local to load the module",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--remote",
        help="Use action load remote to load the module",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    runner = unittest.TextTestRunner(failfast=True, warnings="ignore")
    result = runner.run(test_suite(args))
