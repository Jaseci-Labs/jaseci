from jaseci.element.master import master
from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph
from jaseci.actions.module.ai_serving_api import check_model_live

from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase


class FasttextClfTests(TestCaseHelper, TestCase):
    """Unit tests for fasttext_classifier actions"""

    def setUp(self):
        super().setUp()
        self.master = master(h=mem_hook())
        self.gph = graph(m_id=self.master._m_id, h=self.master._h)
        self.sent = sentinel(m_id=self.master._m_id, h=self.master._h)

    def tearDown(self):
        super().tearDown()

    def test_fasttext_classifier_predict(self):
        """test fasttext_classifier.predict"""
        if (not check_model_live('FASTTEXT_CLASSIFIER')):
            self.skipTest('External resource not available')

        jac_code = """
        walker test_fasttext_classifier {
            can fasttext_classifier.predict;
            has input;

            report fasttext_classifier.predict(input);
        }
        """
        self.sent.register_code(jac_code)
        self.assertTrue(self.sent.is_active)

        walker = \
            self.sent.walker_ids.get_obj_by_name('test_fasttext_classifier')
        self.assertIsNotNone(walker)

        sentences = ['hello', 'Do I need a passport or visa to enter Guyana?']
        walker.prime(self.gph, {'input': sentences})
        result = walker.run()
        for sentence in sentences:
            self.assertIn(sentence, result[0], sentence)
