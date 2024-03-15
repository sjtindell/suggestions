import unittest
from app import app

class RouteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_suggestions_missing_query_parameter(self):
        response = self.app.get('/suggestions')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Missing query parameter'})

    def test_suggestion_with_query_parameters(self):
        response = self.app.get('/suggestions?q=London&latitude=43.70011&longitude=-79.4163')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('suggestions', data)
        self.assertTrue(len(data['suggestions']) > 0, 'No suggestions returned')

if __name__ == '__main__':
    unittest.main()
