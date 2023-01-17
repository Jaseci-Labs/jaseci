import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class TextTopicExtModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextTopicExtModule, cls).setUpClass()
        ret = load_module_actions("jac_nlp.topic_ext")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("topic_ext.jac", "test_topic_ext")
    def test_topic_ext(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(TextTopicExtModule, cls).tearDownClass()
        ret = unload_module("jac_nlp.topic_ext.topic_ext")
        assert ret == True
