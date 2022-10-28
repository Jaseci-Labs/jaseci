from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import (
    load_module_actions,
    load_local_actions,
    load_remote_actions,
)
import unittest
import argparse


class UseEncModule(CoreTest):
    fixture_src = __file__

    def test_load_module(self):
        ret = load_module_actions("jaseci_ai_kit.use_enc")
        self.assertEqual(ret, True)

    def test_load_local(self):
        ret = load_local_actions("jaseci_ai_kit/modules/use_enc/use_enc.py")
        self.assertEqual(ret, True)

    @staticmethod
    def test_load_remote(url):
        def wrapper(args):
            ret = load_remote_actions(url)
            assert ret == True

        return wrapper

    def check_action_modules_module(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertIn("jaseci_ai_kit.modules.use_enc.use_enc", ret)

    def check_action_modules_local(self):
        ret = self.call(self.smast, ["actions_module_list", {}])
        self.assertIn("use_enc.use_enc", ret)

    @jac_testcase("use_enc.jac", "test_enc_cos_sim_score")
    def test_enc_cos_sim_score(self, ret):
        self.assertEqual(round(ret["report"][0], 2), 0.99)

    @jac_testcase("use_enc.jac", "test_enc_text_similarity")
    def test_enc_text_similarity(self, ret):
        self.assertEqual(round(ret["report"][0], 2), 0.03)

    @jac_testcase("use_enc.jac", "test_enc_text_classify")
    def test_enc_text_classify(self, ret):
        self.assertEqual(ret["report"][0]["match"], "getdirections")

    @jac_testcase("use_enc.jac", "test_enc_get_embeddings")
    def test_enc_get_embeddings(self, ret):
        self.assertEqual(len(ret["report"][0][0]), 512)


def test_suite(args):
    suite = unittest.TestSuite()
    load_method = "local" if args.local else ("remote" if args.remote else "module")
    if args.remote:
        suite.addTest(UseEncModule.test_load_remote(url=args.remote))
    else:
        suite.addTest(UseEncModule(f"test_load_{load_method}"))
        suite.addTest(UseEncModule(f"check_action_modules_{load_method}"))
    suite.addTest(UseEncModule("test_enc_cos_sim_score"))
    suite.addTest(UseEncModule("test_enc_text_similarity"))
    suite.addTest(UseEncModule("test_enc_text_classify"))
    suite.addTest(UseEncModule("test_enc_get_embeddings"))
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
        help="Use action load remote to load the module. Need to parse the remote url",
        type=str,
        default=None,
    )
    args = parser.parse_args()

    runner = unittest.TextTestRunner(failfast=True, warnings="ignore")
    result = runner.run(test_suite(args))
    print(
        len(result.errors), len(result.failures), len(result.skipped), result.testsRun
    )
