from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class UseQAModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(UseQAModule, cls).setUpClass()
        ret = load_module_actions("jaseci_ai_kit.use_qa")
        assert ret == True

    @jac_testcase("use_qa.jac", "test_enc_question_similarity")
    def test_enc_question_similarity(self, ret):
        self.assertGreaterEqual(round(ret["report"][0], 2), 0.9)

    @jac_testcase("use_qa.jac", "test_enc_answer_similarity")
    def test_enc_answer_similarity(self, ret):
        self.assertGreaterEqual(round(ret["report"][0], 2), 0.9)

    @jac_testcase("use_qa.jac", "test_enc_question_classify")
    def test_enc_question_classify(self, ret):
        self.assertEqual(ret["report"][0]["match"], "getdirections")

    @jac_testcase("use_qa.jac", "test_enc_answer_classify")
    def test_enc_answer_classify(self, ret):
        self.assertEqual(ret["report"][0]["match"], "searchplace")

    @jac_testcase("use_qa.jac", "test_enc_question")
    def test_enc_question(self, ret):
        self.assertEqual(len(ret["report"][0][0]), 512)

    @jac_testcase("use_qa.jac", "test_enc_answer")
    def test_enc_answer(self, ret):
        self.assertEqual(len(ret["report"][0][0]), 512)

    @jac_testcase("use_qa.jac", "test_enc_qa_classify")
    def test_enc_qa_classify(self, ret):
        self.assertEqual(ret["report"][0]["match"], "searchplace")

    @jac_testcase("use_qa.jac", "test_enc_qa_similarity")
    def test_enc_qa_similarity(self, ret):
        self.assertGreaterEqual(round(ret["report"][0], 2), 0.4)

    @classmethod
    def tearDownClass(cls):
        super(UseQAModule, cls).tearDownClass()
        ret = unload_module("jaseci_ai_kit.modules.use_qa.use_qa")
        assert ret == True
