from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper
import jaseci.actions.live_actions as jla
import jaseci.actions.remote_actions as jra


class jac_actions_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_remote_action_example(self):
        from typing import Union
        @jla.jaseci_action(act_group=['use'], aliases=['enc_question'],
                           allow_remote=True)
        def question_encode(question: Union[str, list]):
            pass

        @jla.jaseci_action(act_group=['use'], aliases=['enc_answer'],
                           allow_remote=True)
        def answer_encode(answer: Union[str, list],
                          context: Union[str, list] = None):
            pass

        @jla.jaseci_action(act_group=['use'],
                           allow_remote=True)
        def cos_sim_score(q_emb: list, a_emb: list):
            pass

        @jla.jaseci_action(act_group=['use'], aliases=['qa_score'],
                           allow_remote=True)
        def dist_score(q_emb: list, a_emb: list):
            pass
        jra.serv_actions()
        self.assertEqual(jra.remote_actions,
                         {'use.answer_encode': ['answer', 'context'],
                          'use.cos_sim_score': ['q_emb', 'a_emb'],
                          'use.dist_score': ['q_emb', 'a_emb'],
                          'use.enc_answer': ['answer', 'context'],
                          'use.enc_question': ['question', ],
                          'use.qa_score': ['q_emb', 'a_emb'],
                          'use.question_encode': ['question']})

    def test_live_action_globals(self):
        self.assertGreater(len(jla.live_actions), 25)
