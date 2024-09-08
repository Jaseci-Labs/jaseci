from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module
import pytest
import os
import shutil
from os import path


class TfmNerTest(CoreTest):
    fixture_src = __file__
    """
    Test Class for Tfm_Ner Module to test the functionality of api's
    """

    @classmethod
    def setUpClass(cls):
        super(TfmNerTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.tfm_ner")
        os.environ["WANDB_DISABLED"] = "true"
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("tfm_ner.jac", "test_train_ner")
    def test_train_ner(self, ret):
        self.assertEqual(ret["success"], True)
        self.assertEqual(ret["report"][0]["status"], "model Training Successful!")

    @pytest.mark.order(2)
    @jac_testcase("tfm_ner.jac", "test_tfm_ner_save_model")
    def test_tfm_ner_save_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(3)
    @jac_testcase("tfm_ner.jac", "test_tfm_ner_load_model")
    def test_tfm_ner_load_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(4)
    @jac_testcase("tfm_ner.jac", "test_extract_entity")
    def test_extract_entity(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(5)
    @jac_testcase("tfm_ner.jac", "test_tfm_ner_get_train_config")
    def test_tfm_ner_get_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(6)
    @jac_testcase("tfm_ner.jac", "test_tfm_ner_set_train_config")
    def test_tfm_ner_set_train_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(7)
    @jac_testcase("tfm_ner.jac", "test_tfm_ner_get_model_config")
    def test_tfm_ner_get_model_config(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(8)
    @jac_testcase("tfm_ner.jac", "test_tfm_ner_set_model_config")
    def test_tfm_ner_set_model_config(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(TfmNerTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.tfm_ner.tfm_ner")
        assert ret is True
        for temp_path in ["results", "modeloutput", "train", "test"]:
            if path.exists(temp_path) and path.isdir(temp_path):
                shutil.rmtree(temp_path)
