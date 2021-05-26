import unittest
from ..t5_app import T5App


class T5RouteTest(unittest.TestCase):
    """Test the route supported by the T5 AI service"""

    def setUp(self):
        self.app = T5App
        self.app.app.config['TESTING'] = True
        self.app.app.config['DEBUG'] = False
        self.client = self.app.app.test_client()

    def tearDown(self):
        pass

    def test_missing_op(self):
        """Test request with missing op field"""
        test_param = {}
        response = self.client.post(
                '/t5/',
                headers={'content-type': 'application/json'},
                json=test_param)
        self.assertEqual(response.status_code, 404)

    def test_invalid_op(self):
        """Test request with invalid op field"""
        test_param = {'op': 'play_poker'}
        response = self.client.post(
                '/t5/',
                headers={'content-type': 'application/json'},
                json=test_param)
        self.assertEqual(response.status_code, 404)

    def test_invalid_request_body(self):
        """Test request with invalid request body"""
        test_param = {'op': 'summarize', 'pic': 2134, 'cats': '212'}
        response = self.client.post(
                '/t5/',
                headers={'content-type': 'application/json'},
                json=test_param)
        self.assertEqual(response.status_code, 404)

    def test_text_only(self):
        """Test valid request with text only, no length params"""
        test_param = {
            'op': 'summarize',
            'text': 'Moderna on Tuesday announced that its coronavirus vaccine '
            'was found to be safe and 100% effective at protecting against '
            'COVID-19 in a Phase 3 trial of more than 3,700 participants between '
            'the ages of 12 and 17. Moderna CEO Stéphane Bancel said the company '
            'plans to submit its data to global regulators in early June, paving '
            'the way for an emergency use authorization for adolescents. If '
            'approved by the U.S. Food and Drug Administration, it would increase '
            'the number of available vaccines for teenagers before the school '
            'year starts, per CNBC. Moderna\'s vaccine is the second to show high '
            'efficacy in younger age groups, following Pfizer, which received an '
            'FDA emergency use authorization for adolescents earlier this '
            'month.',
        }
        response = self.client.post(
                '/t5/',
                headers={'content-type': 'application/json'},
                json=test_param)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('summary' in response.json)
        self.assertTrue(
               10 <= len(response.json['summary'].split(' ')) <= 20)

    def test_text_with_min_max(self):
        """Test valid request with text and min, max length"""
        test_param = {
            'op': 'summarize',
            'text': 'Moderna on Tuesday announced that its coronavirus vaccine '
            'was found to be safe and 100% effective at protecting against '
            'COVID-19 in a Phase 3 trial of more than 3,700 participants between '
            'the ages of 12 and 17. Moderna CEO Stéphane Bancel said the company '
            'plans to submit its data to global regulators in early June, paving '
            'the way for an emergency use authorization for adolescents. If '
            'approved by the U.S. Food and Drug Administration, it would increase '
            'the number of available vaccines for teenagers before the school '
            'year starts, per CNBC. Moderna\'s vaccine is the second to show high '
            'efficacy in younger age groups, following Pfizer, which received an '
            'FDA emergency use authorization for adolescents earlier this '
            'month.',
            'min_length': 20,
            'max_length': 30
        }
        response = self.client.post(
                '/t5/',
                headers={'content-type': 'application/json'},
                json=test_param)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('summary' in response.json)
        self.assertTrue(
               20 <= len(response.json['summary'].split(' ')) <= 30)