from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class EntExtTest(CoreTest):
    fixture_src = __file__
    """
    Test Class for EntExt Module to test the functionality of api's
    """

    @classmethod
    def setUpClass(cls):
        super(EntExtTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.ent_ext")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("ent_ext.jac", "test_ent_ext_set_config")
    def test_ent_ext_set_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(2)
    @jac_testcase("ent_ext.jac", "test_train_ner")
    def test_train_ner(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(3)
    @jac_testcase("ent_ext.jac", "test_extract_entity")
    def test_extract_entity(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(4)
    @jac_testcase("ent_ext.jac", "test_ent_ext_save_model")
    def test_ent_ext_save_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(5)
    @jac_testcase("ent_ext.jac", "test_ent_ext_load_model")
    def test_ent_ext_load_model(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(EntExtTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.ent_ext.ent_ext")
        assert ret is True
