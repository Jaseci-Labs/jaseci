from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class PDFExtModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(PDFExtModule, cls).setUpClass()
        ret = load_module_actions("jac_misc.pdf_ext")
        assert ret == True

    @jac_testcase("pdf_ext.jac", "test_valid_pdf_url")
    def test_valid_pdf_url(self, ret):
        self.assertIn("content", ret["report"][0].keys())

    @jac_testcase("pdf_ext.jac", "test_metadata_enabled")
    def test_metadata_enabled(self, ret):
        self.assertIn("metadata", ret["report"][0].keys())

    @jac_testcase("pdf_ext.jac", "test_metadata_disabled")
    def test_metadata_disabled(self, ret):
        self.assertNotIn("metadata", ret["report"][0].keys())

    @classmethod
    def tearDownClass(cls):
        super(PDFExtModule, cls).tearDownClass()
        ret = unload_module("jac_misc.pdf_ext.pdf_ext")
        assert ret == True
