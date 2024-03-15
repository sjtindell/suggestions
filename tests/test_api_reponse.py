import requests
import unittest

class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_suggestions_endpoint(self):
        url = 'http://127.0.0.1:5000/suggestions'
        params = {
            'q': 'London',
            'latitude': '43.70011',
            'longitude': '-79.4163'
        }

        expected_suggestions = [
            {'latitude': 42.98339, 'longitude': -81.23304, 'name': 'London, 08, CA', 'score': 0.97},
            {'latitude': 39.88645, 'longitude': -83.44825, 'name': 'London, OH, US', 'score': 0.915},
            {'latitude': 37.12898, 'longitude': -84.08326, 'name': 'London, KY, US', 'score': 0.876},
            {'latitude': 44.51422, 'longitude': -72.01093, 'name': 'Lyndon, VT, US', 'score': 0.8},
        ]
        
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('suggestions', data)
        self.assertTrue(len(data['suggestions']) > 0, 'No suggestions returned')
        
        actual_suggestions = data['suggestions'][:4]  # checking the first 4 against expected
        for expected, actual in zip(expected_suggestions, actual_suggestions):
            self.assertAlmostEqual(expected['latitude'], actual['latitude'], places=5)
            self.assertAlmostEqual(expected['longitude'], actual['longitude'], places=5)
            self.assertEqual(expected['name'], actual['name'])
            self.assertAlmostEqual(expected['score'], actual['score'], places=5)

    def test_suggestions_for_london_without_location(self):
        url = 'http://127.0.0.1:5000/suggestions'
        params = {'q': 'London'}  # No latitude or longitude provided
        
        new_expected_suggestions = [
            {'latitude': 42.98339, 'longitude': -81.23304, 'name': 'London, 08, CA', 'score': 1.0},
            {'latitude': 37.12898, 'longitude': -84.08326, 'name': 'London, KY, US', 'score': 1.0},
            {'latitude': 39.88645, 'longitude': -83.44825, 'name': 'London, OH, US', 'score': 1.0},
            {'latitude': 38.25674, 'longitude': -85.60163, 'name': 'Lyndon, KY, US', 'score': 0.83},
        ]

        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('suggestions', data)
        self.assertTrue(len(data['suggestions']) > 0, 'No suggestions returned')
        
        actual_suggestions = data['suggestions'][:4]  # Check the first 4 against expected
        for expected, actual in zip(new_expected_suggestions, actual_suggestions):
            self.assertAlmostEqual(expected['latitude'], actual['latitude'], places=5)
            self.assertAlmostEqual(expected['longitude'], actual['longitude'], places=5)
            self.assertEqual(expected['name'], actual['name'])
            self.assertAlmostEqual(expected['score'], actual['score'], places=2)

    def test_no_suggestions_for_nonexistent_city(self):
        url = 'http://127.0.0.1:5000/suggestions'
        params = {
            'q': 'SomeRandomCityInTheMiddleOfNowhere'
        }
        
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200, 'The request did not succeed')
        
        data = response.json()
        self.assertIn('suggestions', data, "'suggestions' key not in response")
        self.assertEqual(len(data['suggestions']), 0, 'Expected no suggestions, but got some')

if __name__ == '__main__':
    unittest.main()
