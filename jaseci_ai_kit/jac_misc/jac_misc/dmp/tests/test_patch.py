from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import diff_match_patch as dmp_module


class PatchTest(CoreTest):
    """ UnitTest for Match Module """

    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(PatchTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.patch")
        assert ret

    @jac_testcase("patch.jac", "get_text_test")
    def test_get_text(self, ret):
        dmp = dmp_module.diff_match_patch()
        actual = dmp.make_patch("patching file: file 123", "diffing file: file 124")
        self.assertEqual(ret["report"][0], actual)

    @jac_testcase("patch.jac", "get_diff_test")
    def test_get_diff(self, ret):
        dmp = dmp_module.diff_match_patch()
        actual = dmp.make_patch("patching file: file 123", "diffing file: file 124")
        self.assertEqual(ret["report"][0], actual)

    @jac_testcase("patch.jac", "get_both_test")
    def test_get_both(self, ret):
        dmp = dmp_module.diff_match_patch()
        actual = dmp.make_patch("patching file: file 123", "diffing file: file 124")
        self.assertEqual(ret["report"][0], actual)

    @jac_testcase("patch.jac", "apply_test")
    def test_apply(self, ret):
        dmp = dmp_module.diff_match_patch()
        actual = dmp.make_patch("patching file: file 123", "diffing file: file 124")
        patched = dmp.patch_apply(actual, "patching file: file 123")
        self.assertEqual(ret["report"][0], patched)

    @classmethod
    def tearDownClass(cls):
        super(PatchTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.patch.patch")
        assert ret
