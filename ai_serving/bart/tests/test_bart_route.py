import unittest
from ..bart_app import BARTApp


class BartRouteTest(unittest.TestCase):
    """Test the route supported by the BART AI service"""

    def setUp(self):
        self.app = BARTApp
        self.app.app.config['TESTING'] = True
        self.app.app.config['DEBUG'] = False
        self.client = self.app.app.test_client()

    def tearDown(self):
        pass

    def test_missing_op(self):
        """Test request with missing op field"""
        test_param = {}
        response = self.client.post(
                '/bart/',
                headers={'content-type': 'application/json'},
                json=test_param)
        self.assertEqual(response.status_code, 404)

    def test_invalid_op(self):
        """Test request with invalid op field"""
        test_param = {'op': 'play_poker'}
        response = self.client.post(
                '/bart/',
                headers={'content-type': 'application/json'},
                json=test_param)
        self.assertEqual(response.status_code, 404)

    def test_invalid_request_body(self):
        """Test request with invalid request body"""
        test_param = {'op': 'play_poker'}
        test_param = {'op': 'eval_assoc', 'pic': 2134, 'cats': '212'}
        response = self.client.post(
                '/bart/',
                headers={'content-type': 'application/json'},
                json=test_param)
        self.assertEqual(response.status_code, 404)

    def test_single_cat(self):
        """Test valid request with single candidate category"""
        test_param = {
            'op': 'eval_assoc',
            'text': 'exercise for 15 minutes',
            'cats': ['get in shape']
        }
        response = self.client.post(
                '/bart/',
                headers={'content-type': 'application/json'},
                json=test_param)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('sorted_associations' in response.json)
        self.assertEqual(
                response.json['sorted_associations'][0][0],
                'get in shape')
        self.assertIsInstance(
                response.json['sorted_associations'][0][1],
                float)

    def test_multi_cat(self):
        """Test valid request with multiple candidate category"""
        test_param = {
            'op': 'eval_assoc',
            'text': 'exercise for 15 minutes',
            'cats': ['get in shape', 'earn a promotion at work', 'buy a house']
        }
        response = self.client.post(
                '/bart/',
                headers={'content-type': 'application/json'},
                json=test_param)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('sorted_associations' in response.json)
        self.assertEqual(
                len(response.json['sorted_associations']),
                len(test_param['cats']))
        self.assertEqual(
                response.json['sorted_associations'][0][0],
                'get in shape')
